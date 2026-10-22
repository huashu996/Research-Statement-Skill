# Public package privacy

This repository distributes reusable instructions, one formatting helper, and two placeholder DOCX templates. It does not distribute an applicant's CV, correspondence, contact details, academic record, referees, research artifacts, or application history.

The public version uses runtime inputs in place of personal workspace settings. Template cleanup removes author and last-editor properties, document timestamps, thumbnails, custom XML, and editing-session identifiers. Placeholder links use `example.org`.

Keep private inputs, generated applications, evidence logs, render outputs, credentials, and machine-specific configuration outside this repository. The included ignore rules reduce accidental inclusion, but cannot replace reviewing the files being committed.

Before publishing a modified copy, inspect text files and the internal XML, links, comments, media and properties of Office archives. Avoid committing private content even temporarily: deleting a file from the latest revision does not remove it from Git history.

The formatting helper operates on local files. Research and document generation may use tools provided by the host agent environment; this package does not determine that environment's data-processing or retention policies. Sending mail, submitting forms, or uploading private material requires separate user authorization.
