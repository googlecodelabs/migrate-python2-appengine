# Module 9 - Migrate from Python 2 to 3 and Cloud NDB to Cloud Datastore

This repo folder is the corresponding Python 3 code to the [Module 9 codelab](http://g.co/codelabs/pae-migrate-py3dstasks). The tutorial STARTs with the Python 2 code in the [Module 8 repo folder](/mod7-cloudtasks) and leads developers through migrating from Python 2 to 3, Cloud NDB to Cloud Datastore plus any changes from Cloud Tasks v1 to v2, culminating in the code in this folder. One major addition to look for here vs. Module 8 is that App Engine `taskqueue` creates a `default` push queue while Cloud Tasks does not, so that now has to be done in code.

**NOTE: Backport to Python 2**: When migrating this app to Python 3, we added a Python 3 dependency: the `print()` function. If for any reason you need to get back on Python 2 App Engine, you would have to:

  1. Decide on your logging strategy. The Python 2 App Engine runtime now allows writing to `stdout`, so you don't have to revert back to `logging.info()` (or preferred logging level), however writing to `stdout` defaults to `logging.error()`. If that is acceptable and to continue with `print()`, add this import (above all others) at top of `main.py`:

    from __future__ import print_function

  2. Revert back to your Python 2 configuration files. For this app, it would be the Module 8 [`app.yaml`](/blob/master/mod8-cloudtasks/app.yaml) and [`appengine_config.py`](/blob/master/mod8-cloudtasks/appengine_config.py) files.
