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
1. Similarly, [gRPC](http://grpc.io) is used by all [*Google Cloud* client libraries](https://cloud.google.com/apis/docs/cloud-client-libraries), and `grpcio` is the gRPC package for Python and thus required.
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

## Next

From here, there's flexibility as to your next move. Choose any of these options:

- [**Step 2:**](/step2-flask-cloudndb-py3) Port your app to Python 3 to get you on the next generation App Engine runtime as Python 2 has reached its end-of-life.
- [**Step 4:**](/step4-cloudndb-cloudrun-py2) Continue to use NDB but migrate your app to a container executing serverlessly on Cloud Run.
- [**Step 3:**](/step3-flask-datastore-py2) Further modernize Datastore access from Cloud NDB to the (official) Cloud Datastore library (how users *outside of* App Engine access Cloud Datastore).
