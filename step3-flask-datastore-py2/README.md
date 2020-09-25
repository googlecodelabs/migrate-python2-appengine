# Step 3 - Migrate from Google Cloud NDB to Cloud Datastore

## Introduction

While [Cloud NDB](https://cloud.google.com/appengine/docs/standard/python3/migrating-to-cloud-ndb) is a great solution for long-time App Engine developers, it is *not* the primary way all other (non-App Engine) users access [Cloud Datastore](https://cloud.google.com/datastore). Instead, they usually use the standard [Cloud Datastore client library](https://cloud.google.com/datastore/docs/reference/libraries).

Since Cloud NDB is a standalone library and is available for both Python 2 & 3, really *anyone* can use it, but its main purpose is to help original App Engine runtime developers migrate, *not* serve as the expected approach for new code. If you *are* an App Engine developer, perhaps with apps running on both the original and next generation runtimes, and don't plan to use Datastore outside of App Engine, you do *not* need to perform this migration and can happily stay with Cloud NDB.

On the other hand, if you have other apps that use Cloud Datastore, you may consider migrating your App Engine apps from Cloud NDB to Datastore. It'll bring consistency to your codebase, enable code reuse, and hopefully lower the overall maintenance cost because you'll just have the single way to access Datastore (vs. two). Please continue if you fall into this group and wish to migrate from Cloud NDB to Cloud Datastore.

---

## Background

App Engine Datastore started as the bundled NoSQL data storage soluion since App Engine's 2008 [original launch in 2008](http://googleappengine.blogspot.com/2008/04/introducing-google-app-engine-our-new.html). Since then, Datastore has grown up to become its own product, Cloud Datastore, [released in 2013](https://cloudplatform.googleblog.com/2013/05/get-started-with-google-cloud-datastore-nosql-database.html). The next generation of Cloud Datastore [launched in 2017](https://developers.googleblog.com/2017/10/introducing-cloud-firestore-our-new.html) with a product rebrand as [Cloud Firestore](https://cloud.google.com/firestore) to signal its feature integration with the [Firebase real-time database](https://firebase.google.com/products/realtime-database). For backwards-compatibility reasons, Cloud Firestore operates in ["Cloud Firestore in Datastore mode"](https://cloud.google.com/datastore/docs) when accessed from the Cloud NDB or Cloud Datastore client libraries.

---

## Migration

Migrating to Cloud Datastore requires changing how you create Datastore entites (at the user-level), store, and query for them. YMMV depending on how complex your Datastore code is. In our sample app, we attempted to make it as straightforward and "non-invasive" as possible. There's also a minor package swap in your `requirements.txt` file. The steps:

1. Update `requirements.txt` to include the Cloud Datastore library (`google-cloud-datastore`).
1. `app.yaml`, `appengine_config.py`, and `templates/index.html` should remain unchanged from the previous migration step.
    - Ensure `app.yaml` (still) references the 3rd-party bundled packages: `grpcio` and `setuptools`
    - Ensure `appengine_config.py` should (still) use `pkg_resources` and `google.appengine.ext.vendor` to point the app at 3rd-party resources.
1. Update your application to use Cloud Datastore

### Configuration

When you're done with the first step, your `requirements.txt` file should look like this:

    Flask
    google-cloud-datastore

You'll likely have to delete your `lib` folder (to get rid of Cloud NDB and dependencies) and add everything back plus Cloud Datastore and dependences with `pip install -t lib -r requirements.txt`.

`app.yaml`, `appengine_config.py`, and `templates/index.html` should remain unchanged as described in the outline above.

### Switch to Cloud Datastore

#### At-a-glance

<table>
<tr>
<th>Description</th>
<th>Cloud NDB</th>
<th>Cloud Datastore</th>
</tr>
<tr>
<td>Imports</td>
<td>
<pre lang="python">
from flask import Flask, render_template, request
from google.cloud import ndb
</pre>
</td>
<td>
<pre lang="python">
from datetime import datetime
from flask import Flask, render_template, request
from google.cloud import datastore
</pre>
</td>
</tr>
<tr>
<td>Initialization and data model</td>
<td>
<pre lang="python">
app = Flask(__name__)
ds_client = ndb.Client()
&nbsp;
class Visit(ndb.Model):
    visitor   = ndb.StringProperty()
    timestamp = ndb.DateTimeProperty(auto_now_add=True)
</pre>
</td>
<td>
<pre lang="python">
app = Flask(__name__)
ds_client = datastore.Client()
</pre>
</td>
</tr>
<tr>
<td>Datastore access</td>
<td>
<pre lang="python">
def store_visit(remote_addr, user_agent):
    with ds_client.context():
        Visit(visitor='{}: {}'.format(remote_addr, user_agent)).put()
&nbsp;
def fetch_visits(limit):
    with ds_client.context():
        return (v.to_dict() for v in Visit.query().order(
                -Visit.timestamp).fetch_page(limit)[0])
</pre>
</td>
<td>
<pre lang="python">
def store_visit(remote_addr, user_agent):
    entity = datastore.Entity(key=ds_client.key('Visit'))
    entity.update({
        'timestamp': datetime.now(),
        'visitor': '{}: {}'.format(remote_addr, user_agent),
    })
    ds_client.put(entity)
&nbsp;
def fetch_visits(limit):
    query = ds_client.query(kind='Visit')
    query.order = ['-timestamp']
    return query.fetch(limit=limit)
</pre>
</td>
</tr>
</table>

#### Imports

Switching the package import is fairly innocuous, and also `import datetime` as the Datastore library doesn't use property types:

- BEFORE:

```python
from flask import Flask, render_template, request
from google.cloud import ndb
```

- AFTER:

```python
from datetime import datetime
from flask import Flask, render_template, request
from google.cloud import datastore
```

#### Initialization and data model

After initializing Flask, create your Datastore clients in an identical way, but delete the data model class as the Datastore library is more flexible:

- BEFORE:

```python
app = Flask(__name__)
ds_client = ndb.Client()

class Visit(ndb.Model):
    visitor   = ndb.StringProperty()
    timestamp = ndb.DateTimeProperty(auto_now_add=True)
```

- AFTER:

```python
app = Flask(__name__)
ds_client = datastore.Client()
```

#### Datastore access

The Datastore library is more flexible than NDB. For example, a data model class is not required and Python context managers aren't used. With Datastore, create a generic entity, identifying like-types with a "key". Create the data record with a JSON object (Python `dict`) of key-value pairs, then write it to Datastore with the expected `put()`. Querying is similar but more straightforward with Datastore. Here you can see how NDB does things compared to Datastore:

- BEFORE:

```python
def store_visit(remote_addr, user_agent):
    with ds_client.context():
        Visit(visitor='{}: {}'.format(remote_addr, user_agent)).put()

def fetch_visits(limit):
    with ds_client.context():
        return (v.to_dict() for v in Visit.query().order(
                -Visit.timestamp).fetch_page(limit)[0])
```

- AFTER:

```python
def store_visit(remote_addr, user_agent):
    entity = datastore.Entity(key=ds_client.key('Visit'))
    entity.update({
        'timestamp': datetime.now(),
        'visitor': '{}: {}'.format(remote_addr, user_agent),
    })
    ds_client.put(entity)

def fetch_visits(limit):
    query = ds_client.query(kind='Visit')
    query.order = ['-timestamp']
    return query.fetch(limit=limit)
```

---

## Next

From here, you have some several options... you can:

1. Migrate your app to Cloud Run (no example provided, but see `step2a-flask-cloudndb-py2-cloudrun`)
1. Port your app to Python 3 (see `step3-flask-datastore-py3`)
1. Combine both of the above steps (migrate to Python 3 *and* Cloud Run; no example provided but extrapolate from above)
1. Further modernize Datastore access from Cloud Datastore to Cloud Firestore, allowing you to take full advantage of native Firestore features (see `step4-flask-firestore-py2`)
