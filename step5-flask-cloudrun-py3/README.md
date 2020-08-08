# Step 5 (EXTRA) - Migrate from Google App Engine to Cloud Run and port to Python 3 (with Docker)

## Introduction

After migrating to Cloud Run, the only changes that need to be made to port the application to Python 3 is to remove the Unicode string identifiers, and even this is optional as they're ignored by 3.x interpreters.

---

## Migration

Porting from Python 2 to 3 is not within the scope of this tutorial, and our simple sample app is already 2-3 compatible, so the only changes required are in configuration.

1. Designate using Python 3 in your `Dockerfile` if you have one. Buildpacks auto-detect this.
1. Any `.dockerignore` should remain as-is.
1. Optionally remove the Unicode string literal designations in `main.py` (see the `diff`s below)

### Configuration

The only real change for this app is to switch the `Dockerfile FROM` directive from `FROM python:2-slim` to `FROM python:3-slim`.

---

## Summary

For the sample app in this tutorial, the overall contextual set of `diff`s (skipping this `README.md` and nonessential files) looks like this:

    $ diff -c step5-flask-cloudrun-py*
    diff -c step5-flask-cloudrun-py2/Dockerfile step5-flask-cloudrun-py3/Dockerfile
    *** step5-flask-cloudrun-py2/Dockerfile 2020-07-31 18:44:08.000000000 -0700
    --- step5-flask-cloudrun-py3/Dockerfile 2020-07-31 18:44:12.000000000 -0700
    ***************
    *** 1,4 ****
    ! FROM python:2-slim
      WORKDIR /app
      COPY . .
      RUN pip install -r requirements.txt
    --- 1,4 ----
    ! FROM python:3-slim
      WORKDIR /app
      COPY . .
      RUN pip install -r requirements.txt
    diff -c step5-flask-cloudrun-py2/main.py step5-flask-cloudrun-py3/main.py
    *** step5-flask-cloudrun-py2/main.py    2020-08-13 16:22:45.000000000 -0700
    --- step5-flask-cloudrun-py3/main.py    2020-08-13 16:23:19.000000000 -0700
    ***************
    *** 7,21 ****
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
      
    --- 7,21 ----
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
      
    Common subdirectories: step5-flask-cloudrun-py2/templates and step5-flask-cloudrun-py3/templates

Congratulations... this app is fully modernized now, concluding this tutorial.
