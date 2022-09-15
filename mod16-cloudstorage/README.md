# Module 16 - Migrate from App Engine `blobstore` to Cloud Storage

## Migrations

This repo folder is the corresponding code to the [Module 16 codelab](https://codelabs.developers.google.com/codelabs/cloud-gae-python-migrate-16-cloudstorage?utm_source=codelabs&utm_medium=et&utm_campaign=CDR_wes_aap-serverless_mgrcloudstorage_sms_202029&utm_content=-). The tutorial STARTs with the Python 2 code in the [Module 15 repo folder](/mod15-blobstore) and leads developers through a set of migrations, culminating in the code in _this_ folder. In addition to migrating to Cloud Storage, a few others are done to get from Modules 15 to 16... here is the complete list:

1. Migrate from App Engine `webapp2` to Flask
1. Migrate from App Engine `ndb` to Cloud NDB
1. Migrate from App Engine `blobstore` to Cloud Storage

The reason why the web framework requires migration is because `blobstore` has dependencies on `webapp` and `webapp2`, so we could not start directly from a Flask app.

## Python compatibility

This app is fully Python 2-3 compatible. To do a Python 3 deployment of this app:

1. Edit `app.yaml` by enabling/uncommenting the `runtime: python39` line
1. Delete all other lines in `app.yaml` and save
1. Delete `lib` (if present) and `appengine_config.py` (neither used in Python 3)
1. Deploy with `gcloud app deploy`

## Backwards compatibility

One catch with this migration is that `blobstore` has a dependency on `webapp`. By migrating to Cloud Storage, that dependency is not resolved because the app was also migrated from `webapp2` (and `webapp`) to Flask. In real life, there may not be an option to just discard all your data. The [`main.py`](main.py) in this folder is for the easy situation where you _can_, replacing `ndb.BlobKeyProperty` (for Blobstore files) with `ndb.StringProperty` (for Cloud Storage files) in the data model.

For the rest of us, we may need [`main-migrate.py`](main-migrate.py), an alternative version of the application. The data model here maintains a `ndb.BlobKeyProperty` for backwards-compatibility and creates a 4th field for the Cloud Storage filename (`ndb.StringProperty`). Furthermore, an additional `etl_visits()` function is required to consolidate files created with Blobstore _and_ Cloud Storage without changing the HTML template.
