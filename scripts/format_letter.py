"""Apply the agreed letter fonts/justification without rewriting content.

Requires lxml. The output may be a new file or explicitly --in-place.
Titles, metadata, greetings and signature paragraphs retain their alignment.
"""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from lxml import etree
import argparse
import hashlib
import json
import os
import re
import tempfile

W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
NS = {'w': W}
Q = lambda name: f'{{{W}}}{name}'
PARSER = etree.XMLParser(resolve_entities=False, no_network=True)


def font_properties(pr):
    rf = pr.find(Q('rFonts'))
    if rf is None:
        rf = etree.Element(Q('rFonts'))
        pr.insert(0, rf)
    for name in list(rf.attrib):
        if 'theme' in name.lower():
            del rf.attrib[name]
    for name in ('ascii', 'hAnsi', 'cs'):
        rf.set(Q(name), 'Times New Roman')
    rf.set(Q('eastAsia'), 'SimSun')


def ensure_properties(element, tag):
    pr = element.find(Q(tag))
    if pr is None:
        pr = etree.Element(Q(tag))
        element.insert(0, pr)
    return pr


def content_signature(root):
    return root.xpath('//w:t/text() | //w:instrText/text()', namespaces=NS)


def format_letter(source, target, keep_styles=(), keep_prefixes=()):
    with ZipFile(source) as z:
        entries = z.infolist()
        parts = {i.filename: z.read(i.filename) for i in entries}
    original = dict(parts)
    protected_styles = {'Title', 'Subtitle', 'Header', 'Footer', 'Caption', *keep_styles}
    prefixes = ('To:', 'Subject:', 'Dear ', 'Thank you for your consideration.',
                'Best regards', 'Kind regards', 'Sincerely', 'Yours sincerely',
                'Respectfully', '核查日期', '收件人：', '主题：', *keep_prefixes)
    modified = []
    justified = 0
    for name, blob in list(parts.items()):
        if name not in ('word/document.xml', 'word/styles.xml') and not re.fullmatch(r'word/(header|footer)\d+\.xml', name):
            continue
        root = etree.fromstring(blob, PARSER)
        before = content_signature(root)
        for pr in root.findall('.//w:rPr', NS):
            font_properties(pr)
        for run in root.findall('.//w:r', NS):
            font_properties(ensure_properties(run, 'rPr'))
        if name == 'word/styles.xml':
            for style in root.findall('w:style', NS):
                pr = style.find(Q('rPr'))
                if pr is None:
                    pr = etree.SubElement(style, Q('rPr'))
                font_properties(pr)
        if name == 'word/document.xml':
            signature = False
            for p in root.findall('.//w:body//w:p', NS):
                text = ''.join(p.xpath('.//w:t/text()', namespaces=NS)).strip()
                pr = p.find(Q('pPr'))
                style = pr.find(Q('pStyle')) if pr is not None else None
                style_id = style.get(Q('val'), '') if style is not None else ''
                heading = style_id in protected_styles or style_id.lower().startswith('heading')
                page_break = bool(p.xpath('.//w:br[@w:type="page"]', namespaces=NS))
                page_break = page_break or (pr is not None and pr.find(Q('pageBreakBefore')) is not None)
                if heading or page_break:
                    signature = False
                is_signoff = text.startswith(('Best regards', 'Kind regards', 'Sincerely', 'Yours sincerely', 'Respectfully'))
                if is_signoff:
                    signature = True
                if not text or heading or signature or text.startswith(prefixes):
                    continue
                pr = ensure_properties(p, 'pPr')
                jc = pr.find(Q('jc'))
                if jc is None:
                    jc = etree.SubElement(pr, Q('jc'))
                jc.set(Q('val'), 'both')
                justified += 1
        assert content_signature(root) == before, f'Text/field content changed: {name}'
        parts[name] = etree.tostring(root, encoding='UTF-8', xml_declaration=True, standalone=True)
        modified.append(name)
    if 'word/settings.xml' in parts:
        root = etree.fromstring(parts['word/settings.xml'], PARSER)
        compat = root.find(Q('compat'))
        if compat is None:
            compat = etree.SubElement(root, Q('compat'))
        flag = compat.find(Q('doNotExpandShiftReturn'))
        if flag is None:
            flag = etree.SubElement(compat, Q('doNotExpandShiftReturn'))
        flag.set(Q('val'), '1')
        parts['word/settings.xml'] = etree.tostring(root, encoding='UTF-8', xml_declaration=True, standalone=True)
        modified.append('word/settings.xml')
    for name in original.keys() - set(modified):
        assert original[name] == parts[name], f'Unexpected package change: {name}'
    target.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix='letter-format-', suffix='.docx', dir=target.parent)
    os.close(fd)
    temp = Path(temp_name)
    try:
        with ZipFile(temp, 'w', ZIP_DEFLATED) as z:
            for info in entries:
                z.writestr(info, parts[info.filename])
        with ZipFile(temp) as z:
            assert z.testzip() is None, 'Output ZIP corruption'
        os.replace(temp, target)
    finally:
        if temp.exists():
            temp.unlink()
    return {'output': str(target), 'body_paragraphs_justified': justified,
            'text_and_fields_preserved': True, 'links_and_unrelated_parts_preserved': True,
            'sha256': hashlib.sha256(target.read_bytes()).hexdigest()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    parser.add_argument('output', type=Path, nargs='?')
    parser.add_argument('--in-place', action='store_true')
    parser.add_argument('--keep-style', action='append', default=[])
    parser.add_argument('--keep-prefix', action='append', default=[])
    args = parser.parse_args()
    source = args.input.resolve(strict=True)
    if source.suffix.lower() != '.docx':
        parser.error('Input must be a DOCX file')
    if args.in_place:
        if args.output is not None:
            parser.error('Use OUTPUT or --in-place, not both')
        target = source
    else:
        if args.output is None:
            parser.error('Provide OUTPUT or explicitly use --in-place')
        target = args.output.resolve()
        if target == source:
            parser.error('Same input/output requires --in-place')
    if target.suffix.lower() != '.docx':
        parser.error('Output must be a DOCX file')
    print(json.dumps(format_letter(source, target, args.keep_style, args.keep_prefix), ensure_ascii=False))


if __name__ == '__main__':
    main()
