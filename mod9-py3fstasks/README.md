# Module 9 - Migrate from Python 2 to 3 and Cloud NDB to Cloud Firestore

This repo folder is the corresponding Python 3 code to the [Module 9 codelab](http://g.co/codelabs/pae-migrate-py3fstasks). The tutorial STARTs with the Python 2 code in the [Module 8 repo folder](/mod7-cloudtasks) and leads developers through migrating from Python 2 to 3, Cloud NDB to Cloud Firestore (skipping over a Cloud Datstore migration) plus any changes from Cloud Tasks v1 to v2, culminating in the code in this folder. One major addition to look for here vs. Module 8 is that App Engine `taskqueue` creates a `default` push queue while Cloud Tasks does not, so that now has to be done in code.

**NOTE: Batch delete**: The deletion process in this app is "one-at-a-time." If your app requires deletion of more than a few documents, consider switching to the batch model. In this case, you would replace `_delete_docs()` with:

    def _delete_docs(visits):
        'app-internal generator deleting old FS visit documents'
        batch = fs_client.batch()
        for visit in visits:
            batch.delete(visit.reference)
            yield visit.id
        batch.commit()

**NOTE: Backport to Python 2**: When migrating this app to Python 3, we added a Python 3 dependency: the `print()` function. If for any reason you need to get back on Python 2 App Engine, you would have to:

  1. Decide on your logging strategy. The Python 2 App Engine runtime now allows writing to `stdout`, so you don't have to revert back to `logging.info()` (or preferred logging level), however writing to `stdout` defaults to `logging.error()`. If that is acceptable and to continue with `print()`, add a `__future__.print_function` import above the others so the top of `main.py` looks like this:

    from __future__ import print_function
    from datetime import datetime
    import json
    import time
    from flask import Flask, render_template, request
    import google.auth
    from google.cloud import firestore, tasks

  2. Revert back to your Python 2 configuration files. For this app, it would be Module 8's [`app.yaml`](https://github.com/googlecodelabs/migrate-python2-appengine/blob/master/mod8-cloudtasks/app.yaml) and [`appengine_config.py`](https://github.com/googlecodelabs/migrate-python2-appengine/blob/master/mod8-cloudtasks/appengine_config.py) files.

  3. Revert all package versions from `requirements.txt` to get the latest/last(?) package versions for Python 2 as well as run `pip install -t lib -r requirements.txt` again. Here is what ours looks like:

    flask==1.1.2
    google-cloud-firestore==1.9.0
    google-cloud-tasks==1.5.0

