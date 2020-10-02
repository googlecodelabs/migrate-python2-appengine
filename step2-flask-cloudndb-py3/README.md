# Step 2 (EXTRA) - After migrating to Google Cloud NDB, port to Python 3

## Introduction

We recommend developers migrate to Python 3 to access the latest App Engine runtimes & features. Developers can make this migration as soon as they've migrated to Cloud NDB (now). However since this can be a large undertaking, you can move to Py3 after any of the datastore migration steps, not just this one. One of the outstanding features of the App Engine second generation runtimes (Gen2) is that neither "vendored" nor bundled 3rd-party packages are required to be uploaded to the service. They are automatically installed directly from `requirements.txt`.

---

## Migration

Porting from Python 2 to 3 is not within the scope of this tutorial, and our simple sample app is already 2-3 compatible, so the only changes required are in configuration:

1. Simplify `app.yaml` to reference Python 3 and remove reference to bundled 3rd-party libraries.
1. Delete `appengine_config.py` as it's no longer necessary.
1. Delete the `lib` folder for the same reason.
1. Migrate from App Engine NDB to Cloud NDB

### Configuration

The only real change for this sample app is to significantly shorten `app.yaml` down to just these lines for the runtime as well as routing:

```yml
runtime: python38

handlers:
- url: /.*
  script: auto
```

`requirements.txt` and `templates/index.html` remain unchanged while the `appengine_config.py` file and `lib` folder are deleted.

---

## Next

From here, your options are:

- [**Step 4:**](/step4-cloudds-cloudrun-py3) Migrate your app to a container executing serverlessly on Cloud Run
- [**Step 3:**](/step3-flask-datastore-py3) Further modernize Datastore access from Cloud NDB to the (official) Cloud Datastore library (how users *outside of* App Engine access Cloud Datastore)