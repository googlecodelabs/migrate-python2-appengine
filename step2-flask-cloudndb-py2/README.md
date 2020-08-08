# Step 2 - Migrate from App Engine NDB to Google Cloud NDB

## Introduction

With the web framework port out of the way, we can now focus on upgrading the use of App Engine built-in services libraries. In the case for this tutorial, it's merely a switch from App Engine's `ndb` library to the Cloud NDB library.

Completing this migration opens many doors for developers. Users can then:
- Migrate from Python 2 to Python 3 & the next generation App Engine runtime (Gen2)
- Migrate to the standard Cloud Datastore library all non-App Engine users use
- Containerize their Python 2 app and migrate immediately to Cloud Run

---

## Migration

App Engine services have blossomed into their own products, and App Engine's Datastore is no exception. Switching from App Engine `ndb` to Cloud NDB libraries requires inclusion of the (now-external) Cloud NDB client library as well as a minor tweak to Datastore access:

1. Update `requirements.txt` to include the Cloud NDB library (`google-cloud-ndb`).
1. Update `app.yaml` to reference a pair of 3rd-party bundled packages: `grpcio` and `setuptools`
1. Update `appengine_config.py` to use the `pkg_resources` tool (which comes with `setuptools`) so App Engine can access [3rd-party libraries already available on Google servers](https://cloud.google.com/appengine/docs/standard/python/tools/built-in-libraries-27) so users don't have to list them in `requirements.txt` nor `pip install` them.
1. Switch application code to use the Cloud NDB client library

### Configuration

When you're done with the first step, your `requirements.txt` file should look like this:

    Flask
    google-cloud-ndb

Run `pip install -t lib -r requirements.txt` to add Cloud NDB to your `lib` folder. Note you'll get warnings for the previously-installed packages. To avoid this, add a `-U` option to force replacing those libraries (`pip install -U -t lib -r requirements.txt`). Once you're done, `lib` should have many more packages (these are *in addition to* the ones installed previously):

    cachetools/
    cachetools-3.1.1.dist-info/
    certifi/
    certifi-2020.6.20.dist-info/
    chardet/
    chardet-3.0.4.dist-info/
    concurrent/
    easy_install.py
    easy_install.pyc
    enum/
    enum34-1.1.10.dist-info/
    futures-3.3.0.dist-info/
    google/
    google_api_core-1.22.0.dist-info/
    google_api_core-1.22.0-py3.8-nspkg.pth
    googleapis_common_protos-1.52.0.dist-info/
    googleapis_common_protos-1.52.0-py3.8-nspkg.pth
    google_auth-1.20.0.dist-info/
    google_auth-1.20.0-py3.8-nspkg.pth
    google_cloud_core-1.3.0.dist-info/
    google_cloud_core-1.3.0-py3.8-nspkg.pth
    google_cloud_datastore-1.13.2.dist-info/
    google_cloud_datastore-1.13.2-py3.8-nspkg.pth
    google_cloud_ndb-1.4.1.dist-info/
    google_cloud_ndb-1.4.1-py2.7-nspkg.pth
    grpc/
    grpcio-1.30.0.dist-info/
    idna/
    idna-2.10.dist-info/
    pkg_resources/
    protobuf-3.12.2.dist-info/
    protobuf-3.12.2-py2.7-nspkg.pth
    pyasn1/
    pyasn1-0.4.8.dist-info/
    pyasn1_modules/
    pyasn1_modules-0.2.8.dist-info/
    pytz/
    pytz-2020.1.dist-info/
    redis/
    redis-3.5.3.dist-info/
    requests/
    requests-2.24.0.dist-info/
    rsa/
    rsa-4.5.dist-info/
    setuptools/
    setuptools-44.1.1.dist-info/
    six-1.15.0.dist-info/
    six.py
    six.pyc
    urllib3/
    urllib3-1.25.10.dist-info/

After the next step, `app.yaml` should have a new `libraries` section:

```yml
libraries:
- name: grpcio
  version: 1.0.0
- name: setuptools
  version: 36.6.0
```

Update `appengine_config.py` to use `pkg_resources`:

```python
import pkg_resources
from google.appengine.ext import vendor

# Set PATH to your libraries folder.
PATH = 'lib'
# Add libraries installed in the PATH folder.
vendor.add(PATH)
# Add libraries to pkg_resources working set to find the distribution.
pkg_resources.working_set.add_entry(PATH)
```

### Port from App Engine NDB to Cloud NDB

#### Imports

Switching the package import is fairly innocuous:

- BEFORE

```python
from google.appengine.ext import ndb
```

- AFTER:

```python
from google.cloud import ndb
```

#### Datastore access

Using context managers is required by the library for all Datastore access. If you're unfamiliar with [Python context managers](https://docs.python.org/3/reference/datamodel.html#context-managers), their purpose is to "gate" access to resources such that they must be acquired before they can be used. Based on the Computer Science control technique known as [Resource Allocation Is Initialization (or RAII)](https://wikipedia.org/wiki/Resource_acquisition_is_initialization), this technique is also used for files (must be opened before they can be accessed), [spin locks](https://wikipedia.org/wiki/Spinlock) (which must be obtained before entering a ["critical section"](https://wikipedia.org/wiki/Critical_section) of code, etc.

The Cloud NDB requires you create a client to communicate with the API; do that with `ds_client = ndb.Client()` and wrap the code blocks accessing the Datastore with `with` statements that request the context manager:

- BEFORE:

```python
def store_visit(remote_addr, user_agent):
    Visit(visitor='{}: {}'.format(remote_addr, user_agent)).put()

def fetch_visits(limit):
    return (v.to_dict() for v in Visit.query().order(
        -Visit.timestamp).fetch_page(limit)[0])
```

- AFTER:

```python
def store_visit(remote_addr, user_agent):
    with ds_client.context():
        Visit(visitor='{}: {}'.format(remote_addr, user_agent)).put()

def fetch_visits(limit):
    with ds_client.context():
        return (v.to_dict() for v in Visit.query().order(
                -Visit.timestamp).fetch_page(limit)[0])
```

---

## Summary

For this migration step, here are the contextual `diff`s:

    $ diff -c step[12]*py2
    diff -c step1-flask-gaendb-py2/app.yaml step2-flask-cloudndb-py2/app.yaml
    *** step1-flask-gaendb-py2/app.yaml     2020-07-25 14:10:53.000000000 -0700
    --- step2-flask-cloudndb-py2/app.yaml   2020-08-05 00:09:42.000000000 -0700
    ***************
    *** 5,7 ****
    --- 5,13 ----
      handlers:
      - url: /.*
        script: main.app
    + 
    + libraries:
    + - name: grpcio
    +   version: 1.0.0
    + - name: setuptools
    +   version: 36.6.0
    diff -c step1-flask-gaendb-py2/appengine_config.py step2-flask-cloudndb-py2/appengine_config.py
    *** step1-flask-gaendb-py2/appengine_config.py  2020-07-24 23:09:45.000000000 -0700
    --- step2-flask-cloudndb-py2/appengine_config.py        2020-07-24 22:50:57.000000000 -0700
    ***************
    *** 1,6 ****
    --- 1,9 ----
    + import pkg_resources
      from google.appengine.ext import vendor
      
      # Set PATH to your libraries folder.
      PATH = 'lib'
      # Add libraries installed in the PATH folder.
      vendor.add(PATH)
    + # Add libraries to pkg_resources working set to find the distribution.
    + pkg_resources.working_set.add_entry(PATH)
    diff -c step1-flask-gaendb-py2/main.py step2-flask-cloudndb-py2/main.py
    *** step1-flask-gaendb-py2/main.py      2020-07-25 13:58:18.000000000 -0700
    --- step2-flask-cloudndb-py2/main.py    2020-07-25 14:00:56.000000000 -0700
    ***************
    *** 1,18 ****
      from flask import Flask, render_template, request
    ! from google.appengine.ext import ndb
      
      app = Flask(__name__)
      
      class Visit(ndb.Model):
          visitor   = ndb.StringProperty()
          timestamp = ndb.DateTimeProperty(auto_now_add=True)
      
      def store_visit(remote_addr, user_agent):
    !     Visit(visitor='{}: {}'.format(remote_addr, user_agent)).put()
      
      def fetch_visits(limit):
    !     return (v.to_dict() for v in Visit.query().order(
    !         -Visit.timestamp).fetch_page(limit)[0])
      
      @app.route('/')
      def root():
    --- 1,21 ----
      from flask import Flask, render_template, request
    ! from google.cloud import ndb
      
      app = Flask(__name__)
    + ds_client = ndb.Client()
      
      class Visit(ndb.Model):
          visitor   = ndb.StringProperty()
          timestamp = ndb.DateTimeProperty(auto_now_add=True)
      
      def store_visit(remote_addr, user_agent):
    !     with ds_client.context():
    !         Visit(visitor='{}: {}'.format(remote_addr, user_agent)).put()
      
      def fetch_visits(limit):
    !     with ds_client.context():
    !         return (v.to_dict() for v in Visit.query().order(
    !                 -Visit.timestamp).fetch_page(limit)[0])
      
      @app.route('/')
      def root():
    diff -c step1-flask-gaendb-py2/requirements.txt step2-flask-cloudndb-py2/requirements.txt
    *** step1-flask-gaendb-py2/requirements.txt     2020-07-24 19:27:45.000000000 -0700
    --- step2-flask-cloudndb-py2/requirements.txt   2020-07-24 21:59:58.000000000 -0700
    ***************
    *** 1 ****
    --- 1,2 ----
      Flask
    + google-cloud-ndb
    Common subdirectories: step1-flask-gaendb-py2/templates and step2-flask-cloudndb-py2/templates

From here, you have some flexibility as to your next move. You can...

- Continue to use NDB but migrate your app to a container executing serverlessly on Cloud Run (see `step2a-flask-cloudndb-py2-cloudrun`)
- Port your app to Python 3 (see `step2-flask-cloudndb-py3`)
- Combine both of the above steps (migrate to Python 3 *and* Cloud Run; no example provided but extrapolate from above)
- Further modernize Datastore access from Cloud NDB to the (official) Cloud Datastore library (how users *outside of* App Engine access Cloud Datastore) (see `step3-flask-datastore-py2`)
