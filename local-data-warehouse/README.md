# Local Data Warehouse

This is a directory for storing local data files used during manual curation.
Here, a curator can store any input and output to the curation effort of a dataset.

This directory is intended to be backed up to a cloud storage service to ensure data safety.
Furthermore, curators can download from this storage to inspect and re-work on datasets as needed.



## Example code to upload to a GCP bucket:

```bash
gsutil -m rsync -r ./local_folder gs://your-bucket/path/ 
```