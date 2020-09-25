# Step 3 (EXTRA) - After migrating to Cloud Datastore, port to Python 3

## Introduction

The purpose of this tutorial is to helps you port to Python 3 after your migration to Cloud Datastore. We recommend developers migrate to Python 3 to access the latest App Engine runtimes & features. However since this is a large undertaking, you can move to Py3 after any of the datastore migration steps, not just this one. One of the outstanding features of the App Engine second generation runtimes (Gen2) is that neither "vendored" nor bundled 3rd-party packages are required to be uploaded to the service. They are automatically installed directly from `requirements.txt`.

If you have already migrated to Python 3 from an earlier step, see the `README.md` file for the Python 2 version of this step to get a better understanding as to what all the migration steps are. The remainder of this content is focused only only migrating from Python 2 to 3.

---

## Migration

Porting from Python 2 to 3 is not within the scope of this tutorial, and our simple sample app is already 2-3 compatible, so the only changes required are in configuration.

1. Simplify `app.yaml` to reference Python 3 and remove reference to bundled 3rd-party libraries.
1. Delete `appengine_config.py` and the `lib` folder as they're no longer necessary.
1. Independently migrate your application to Python 3

### Configuration

The only real change for this sample app is to significantly shorten `app.yaml` down to just these lines for the runtime as well as routing:

```yml
runtime: python38

handlers:
- url: /.*
  script: auto
```

`requirements.txt` and HTML `templates/index.html` remain unchanged while the `appengine_config.py` file and `lib` folder are deleted.

---

## Next

From here, your options are:

1. Migrate your app to Cloud Run (no example provided, but see `step2a-flask-cloudndb-py2-cloudrun`)
1. Further modernize Datastore access to Cloud Firestore, allowing you to take full advantage of native Firestore features (see `step4-flask-firestore-py3` and the `README.md` in `step4-flask-firestore-py2`).
