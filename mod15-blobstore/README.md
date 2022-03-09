# Module 15 - Add usage of App Engine `blobstore` to baseline sample app (Module 0)

This repo folder is the corresponding code to the [Module 14 codelab](http://g.co/codelabs/pae-migrate-blobstore). The tutorial STARTs with the Python 2 code in the [Module 0 repo folder](/mod0-baseline) and leads developers through adding use of App Engine `blobstore`. Unlike other sample apps, this does not use the default Django templating system, but instead, uses Jinja2, which is supported in `webapp2_extras`.

Blobstore evolved into [Google Cloud Storage](https://cloud.google.com/storage), and all blobs/files created using the Blobstore API go into the default Cloud Storage bucket for your Cloud project, which is the project's ID, meaning it's your `appspot` domain name, e.g., for project `my-project`, your default bucket would be `my-project.appspot.com`. It is programmatically accessible via `google.appengine.api.app_identity.get_default_gcs_bucket_name()`.

The primary application file [`main.py`](main.py) writes files directly to the default bucket. If you want to customize the GCS location where App Engine writes files, see the alternative [`main-gcs.py`](main-gcs.py) file. It uses `google.appengine.api.app_identity.get_default_gcs_bucket_name()` along with the `gs_bucket_name` parameter when calling `google.appengine.ext.blobstore.create_upload_url()`.

Unlike some of the other migrations, Blobstore usage depends on the `webapp` and `webapp2`, so this migration must start at Module 0 rather than Module 1. One update however, is that this sample does use the [Jinja2 templating system](https://jinja.palletsprojects.com) rather than the default Django templates used in Module 0. It is supported in `webapp2` via the `webapp2_extras` package.
