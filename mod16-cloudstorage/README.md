# Module 16 - Migrate from App Engine `blobstore` to Cloud Storage

This repo folder is the corresponding code to the [Module 16 codelab](http://g.co/codelabs/pae-migrate-blobstore). The tutorial STARTs with the Python 2 code in the [Module 15 repo folder](/mod15-blobstore) and leads developers through a set of migrations, culminating in the code in this folder. In addition to migrating to Cloud Storage, a few others are done to get from Modules 15 to 16... here is the complete list:

1. Migrate from App Engine `webapp2` to Flask
1. Migrate from App Engine `ndb` to Cloud NDB
1. Migrate from App Engine `blobstore` to Cloud Storage

The reason why the web framework requires migration is because `blobstore` has dependencies on `webapp` and `webapp2`, so we could not start directly from a Flask app.

This app is fully Python 2-3 compatible. To do a Python 3 deployment of this app:

1. Edit `app.yaml` by enabling/uncommenting the `runtime: python39` line
1. Delete all other lines in `app.yaml`, save, and deploy with `gcloud app deploy`
