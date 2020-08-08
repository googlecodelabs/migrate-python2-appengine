# Step 4 (EXTRA) - After migrating to Cloud Firestore, port to Python 3

## Introduction


The purpose of this tutorial is to helps you port to Python 3 after your migration to Cloud Firestore. We recommend developers migrate to Python 3 to access the latest App Engine runtimes & features. However since this is a large undertaking, you can move to Py3 after any of the datastore migration steps, not just this one. One of the outstanding features of the App Engine second generation runtimes (Gen2) is that neither "vendored" nor bundled 3rd-party packages are required to be uploaded to the service. They are automatically installed directly from `requirements.txt`.

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

## Summary

For the sample app in this tutorial, the overall contextual set of `diff`s (skipping this `README.md` and nonessential files) looks like this:

    $ diff -c step4-flask-firestore-py?
    diff -c step4-flask-firestore-py2/app.yaml step4-flask-firestore-py3/app.yaml
    *** step4-flask-firestore-py2/app.yaml  2020-07-29 21:29:50.000000000 -0700
    --- step4-flask-firestore-py3/app.yaml  2020-07-24 23:59:03.000000000 -0700
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
    Only in step4-flask-firestore-py2: appengine_config.py
    diff -c step4-flask-firestore-py2/main.py step4-flask-firestore-py3/main.py
    *** step4-flask-firestore-py2/main.py   2020-08-13 16:22:34.000000000 -0700
    --- step4-flask-firestore-py3/main.py   2020-08-13 16:22:37.000000000 -0700
    ***************
    *** 6,20 ****
      fs_client = firestore.Client()
      
      def store_visit(remote_addr, user_agent):
    !     doc_ref = fs_client.collection(u'Visit')
          doc_ref.add({
    !         u'timestamp': datetime.now(),
    !         u'visitor': u'{}: {}'.format(remote_addr, user_agent),
          })
      
      def fetch_visits(limit):
    !     visits_ref = fs_client.collection(u'Visit')
    !     visits = (v.to_dict() for v in visits_ref.order_by(u'timestamp',
                  direction=firestore.Query.DESCENDING).limit(limit).stream())
          return visits
      
    --- 6,20 ----
      fs_client = firestore.Client()
      
      def store_visit(remote_addr, user_agent):
    !     doc_ref = fs_client.collection('Visit')
          doc_ref.add({
    !         'timestamp': datetime.now(),
    !         'visitor': '{}: {}'.format(remote_addr, user_agent),
          })
      
      def fetch_visits(limit):
    !     visits_ref = fs_client.collection('Visit')
    !     visits = (v.to_dict() for v in visits_ref.order_by('timestamp',
                  direction=firestore.Query.DESCENDING).limit(limit).stream())
          return visits
      
    Common subdirectories: step4-flask-firestore-py2/templates and step4-flask-firestore-py3/templates

From here, your options are:

1. Migrate your app to Cloud Run (see `step5-flask-cloudrun-py3`)
