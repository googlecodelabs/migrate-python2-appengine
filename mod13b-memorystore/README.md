# Module 13 - Migrate from App Engine `memcache` to Cloud Memorystore

This repo folder is the corresponding Python 3 version of the Module 13 app.

- All files in this folder are identical to the _Python 2_ code in the [Module 13a repo folder](/mod13a-memorystore) **except**:
    1. `app.yaml` was modified for the Python 3 runtime.
    1. `appengine_config.py` is unused and thus deleted.
- An optional migration from Cloud NDB to Cloud Datastore can be achieved via the content covered in [Module 3](http://g.co/codelabs/pae-migrate-datastore).
- The _Python 3_ version of the Module 12 app ([Module 12b repo folder](/mod12b-memcache)) features additional code to support those App Engine legacy ("bundled") services (like `memcache`). Because the app in this folder does not use such services (moved to Cloud Memorystore), that extra support does not appear, so the code here should not be considered a direct migration of that app to Cloud Memorystore (and Cloud NDB), unlike the Python 2 equivalents (Modules [12a](/mod12-memcache) and [13a](/mod13a-memorystore)) which can.
