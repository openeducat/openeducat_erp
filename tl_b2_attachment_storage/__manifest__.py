{
    "name": "TrueLearners Backblaze B2 Attachment Storage",
    "summary": "Store OpenEduCat attachments in a private Backblaze B2 bucket",
    "version": "19.0.1.0.0",
    "category": "Technical",
    "license": "AGPL-3",
    "author": "TrueLearners",
    "depends": [
        "fs_attachment_s3_environment",
    ],
    "post_init_hook": "post_init_hook",
    "installable": True,
    "application": False,
}
