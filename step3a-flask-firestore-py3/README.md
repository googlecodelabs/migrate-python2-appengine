# Step 3a (EXTRA) - Migrate from Google Cloud Datastore to Cloud Firestore

## Introduction

As mentioned in the previous step, a migration to [Cloud Datastore](https://cloud.google.com/datastore) means applications are using "[Cloud Firestore in Datastore mode](https://cloud.google.com/datastore/docs)". The primary purpose of this tutorial is to give developers an idea of the differences between Cloud Datastore as they know it who want to gain initial familiarity with Cloud Firestore.

**This migration is not one we expect users to perform**, which is why it is optional and a "bonus" step. While there are obvious advantages to using [Cloud Firestore](https://cloud.google.com/firestore) natively such as client auth, Firebase rules integration, and of course, the [Firebase realtime ](https://firebase.google.com/products/realtime-database) feature (_query/document watch_), the migration steps are non-trivial:

- You **must** create a new project as once data is stored, projects cannot switch from Datastore (in Firebase mode) to Firestore (native mode).
- There isn't a migration tool that can stream data from one project to another.
- Some critical Datastore features, including namespaces and a higher write throughput (>10k/s), are **not** available from Firestore.
- The export and import tools are "primitive" and "all of nothing" scenarios...
    - If your Datastore is large, it can possibly take many hours to export then import into Firestore
    - During this time, your application/service won't be able write/update data.
    - Migration activities count towards normal usage; you may want to spread it out (across daily quotas if possible) to minimize costs.
    - Because the updated service runs in a different project, you'll need a window for DNS updates to propagate.
-  Datastore & Firestore have similar but different data models so migration requires updating how the app/service works
    - _Ancestor queries_ from Datastore are now _Collection queries_ (the default)
    - Broad type queries from Datastore are Firestore _Collection group queries_
    - Indexes and handling are different, etc.

That said, if you have a trivially-simple app to migrate or are here to learn about the differences between using Datastore vs. Firestore, and wish to use this tutorial as an exercise to achieve that goal, please continue.

> **NOTE:** We present this very optional migration only in Python 3, but you can certainly interpolate and do so with Python 2 where the only difference is that for compatibility reasons, Firestore records use Unicode strings, hence a `u''` leading indicator is needed in front of the Python 2 string literals. For example, the `store_visit()` function will look like the below (vs. in the `main.py` featured in this repo where such directives aren't present).

```python
def store_visit(remote_addr, user_agent):
    doc_ref = fs_client.collection(u'Visit')
    doc_ref.add({
        u'timestamp': datetime.now(),
        u'visitor': u'{}: {}'.format(remote_addr, user_agent),
    })
```

---

## Background

The next generation of Cloud Datastore [launched in 2017](https://developers.googleblog.com/2017/10/introducing-cloud-firestore-our-new.html) with a product rebrand as [Cloud Firestore](https://cloud.google.com/firestore) to signal its feature integration with Firebase. However, users whose migrations are fairly sizable or switching to Gen2 & Python 3 where a new project may be desired have the option of switching to Cloud Firestore natively to take advantage of its full capabilities. See [this document](https://cloud.google.com/datastore/docs/firestore-or-datastore) on choosing between Cloud Firestore in Datastore mode or native Firestore mode.

> **NOTE:** Cloud Firestore is the *only* NoSQL datastore system available to GCP projects, so users [must choose between](https://cloud.google.com/datastore/docs/firestore-or-datastore#choosing_a_database_mode) Firestore in native mode or in Datastore mode; you can't use both Datastore *and* Firestore in the same project.

---

## Migration

Now let's "unmask" Firestore: a Datastore entity is equivalent to a Firestore ["Document"](https://cloud.google.com/firestore/docs/data-model#documents). The key used to group similar entities is a Firestore ["Collection"](https://cloud.google.com/firestore/docs/data-model#collections) (of Documents). Migrating from Datastore requires you to think about these differences because they will materialize when you're creating data records as well as querying for them. YMMV ("your mileage may vary") depending on how complex your Datastore code is. The sample app we use is simplistic enough to experience a straightforward migration.

1. Update `requirements.txt` to include the Cloud Firestore library (`google-cloud-firestore`).
1. `app.yaml`, `appengine_config.py`, and `templates/index.html` should remain unchanged from the previous migration step.
    - Ensure `app.yaml` (still) references the 3rd-party bundled packages: `grpcio` and `setuptools`
    - Ensure `appengine_config.py` should (still) use `pkg_resources` and `google.appengine.ext.vendor` to point the app at 3rd-party resources.
1. Update your application to use Cloud Firestore

### Configuration

When you're done with the first step, your `requirements.txt` file should look like this:

    Flask
    google-cloud-firestore

You'll likely have to delete your `lib` folder (to get rid of Cloud Datastore and dependencies) and add everything back plus Cloud Firestore and dependences with `pip install -t lib -r requirements.txt`.

`app.yaml`, `appengine_config.py`, and `templates/index.html` should remain unchanged as described in the outline above.

### Switch to Cloud Firestore

#### At-a-glance

<table>
<tr>
<th>Description</th>
<th>Cloud Datastore</th>
<th>Cloud Firestore</th>
</tr>
<tr>
<td>Imports</td>
<td>
<pre lang="python">
from google.cloud import datastore
</pre>
</td>
<td>
<pre lang="python">
from google.cloud import firestore
</pre>
</td>
</tr>
<tr>
<td>Initialization</td>
<td>
<pre lang="python">
app = Flask(__name__)
ds_client = datastore.Client()
</pre>
</td>
<td>
<pre lang="python">
app = Flask(__name__)
fs_client = firestore.Client()
</pre>
</td>
</tr>
<tr>
<td>Firestore access</td>
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
<td>
<pre lang="python">
def store_visit(remote_addr, user_agent):
    doc_ref = fs_client.collection('Visit')
    doc_ref.add({
        'timestamp': datetime.now(),
        'visitor': '{}: {}'.format(remote_addr, user_agent),
    })
&nbsp;
def fetch_visits(limit):
    visits_ref = fs_client.collection('Visit')
    visits = (v.to_dict() for v in visits_ref.order_by('timestamp',
            direction=firestore.Query.DESCENDING).limit(limit).stream())
    return visits
</pre>
</td>
</tr>
</table>

#### Imports

Switching the package import is a 4-character change:

- BEFORE:

```python
from google.cloud import datastore
```

- AFTER:

```python
from google.cloud import firestore
```

#### Firestore access

After initializing Flask, create your Firestore client in the same way you did for Datastore (we added a slight change of variable name):

- BEFORE:

```python
app = Flask(__name__)
ds_client = datastore.Client()
```

- AFTER:

```python
app = Flask(__name__)
fs_client = firestore.Client()
```

By performing the migration from Cloud NDB to Cloud Datastore, you've already done the heavylifting to get to Cloud Firestore. Rather than setting a "key" for your entities, you put them in a Firestore collection with the key name. Notice how similar adding new data records are below.

[Querying data in Firestore](https://cloud.google.com/firestore/docs/query-data/queries) is fairly flexible, also as shown below, but could be slightly more verbose as in our sample app. Ironically, Firestore's querying style resembles Cloud NDB more than it does Cloud Datastore.

- BEFORE:

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


- AFTER:

```python
def store_visit(remote_addr, user_agent):
    doc_ref = fs_client.collection('Visit')
    doc_ref.add({
        'timestamp': datetime.now(),
        'visitor': '{}: {}'.format(remote_addr, user_agent),
    })

def fetch_visits(limit):
    visits_ref = fs_client.collection('Visit')
    visits = (v.to_dict() for v in visits_ref.order_by('timestamp',
            direction=firestore.Query.DESCENDING).limit(limit).stream())
    return visits
```

---

## Next

From here, you have some flexibility as to your next move. You can...

1. Migrate your app to Cloud Run (`step5-flask-cloudrun-py2`).
1. Port your app to Python 3 (see `step4-flask-firestore-py3`)
1. Combine both of the above steps (migrate to Python 3 *and* Cloud Run; no example provided but extrapolate from above)
