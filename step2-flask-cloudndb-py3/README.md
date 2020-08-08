# Step 2 (EXTRA) - After migrating to Google Cloud NDB, port to Python 3

## Introduction

We recommend developers migrate to Python 3 to access the latest App Engine runtimes & features. Developers can make this migration as soon as they've migrated to Cloud NDB (now). However since this is a large undertaking, you can move to Py3 after any of the datastore migration steps, not just this one. One of the outstanding features of the App Engine second generation runtimes (Gen2) is that neither "vendored" nor bundled 3rd-party packages are required to be uploaded to the service. They are automatically installed directly from `requirements.txt`.

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

## Summary

For the sample app in this tutorial, the overall contextual set of `diff`s (skipping this `README.md` and nonessential files) looks like this:

    $ diff -c step2-flask-cloudndb-py?
    diff -c step2-flask-cloudndb-py2/app.yaml step2-flask-cloudndb-py3/app.yaml
    *** step2-flask-cloudndb-py2/app.yaml   2020-08-05 00:09:42.000000000 -0700
    --- step2-flask-cloudndb-py3/app.yaml   2020-07-24 23:59:03.000000000 -0700
    ***************
    *** 1,13 ****
    ! runtime: python27
    ! threadsafe: yes
    ! api_version: 1
      
      handlers:
      - url: /.*
    !   script: main.app
    ! 
    ! libraries:
    ! - name: grpcio
    !   version: 1.0.0
    ! - name: setuptools
    !   version: 36.6.0
    --- 1,5 ----
    ! runtime: python38
      
      handlers:
      - url: /.*
    !   script: auto
    Only in step2-flask-cloudndb-py2: appengine_config.py
    Common subdirectories: step2-flask-cloudndb-py2/templates and step2-flask-cloudndb-py3/templates

From here, your options are:

1. Migrate to Cloud Run (no example provided, but see: `step2a-flask-cloudndb-py2-cloudrun`)
1. Further modernize Datastore access to Cloud Datastore (see `step3-flask-datastore-py3` and the `README.md` in `step3-flask-datastore-py2`).
