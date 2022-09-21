# Module 21 - Migrate from App Engine `users` to Cloud Identity Platform

This repo folder is the corresponding Python 3 version of the Module 21 app.

- All files in this folder are identical to the _Python 2_ code in the [Module 21a repo folder](/mod21a-idenplat) **except**:
    1. `app.yaml` was modified for the Python 3 runtime.
    1. `appengine_config.py` is unused and thus deleted.
- An optional migration from Cloud NDB to Cloud Datastore can be achieved via the content covered in [Module 3](http://g.co/codelabs/pae-migrate-datastore).
- The _Python 3_ version of the Module 20 app ([Module 20b repo folder](/mod20b-gaeusers)) features additional code to support those App Engine legacy ("bundled") services (like `memcache`). Because the app in this folder does not use such services (moved to Cloud Memorystore), that extra support does not appear, so the code here should not be considered a direct migration of that app to Cloud Memorystore (and Cloud NDB), unlike the Python 2 equivalents (Modules [20](/mod20-gaeusers) and [21a](/mod21a-idenplat)) which can.
