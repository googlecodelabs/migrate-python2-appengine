# Step 5c - Migrate from Python 2 to 3 and Cloud NDB to Cloud Datastore

## Introduction

The goal of the Step 5 series of codelabs and repos like this is to help App Engine developers migrate from [Python 2 App Engine (Push) Task Queues](https://cloud.google.com/appengine/docs/standard/python/taskqueue/push) to [Google Cloud Tasks](https://cloud.google.com/tasks). They are meant to be *complementary* to the official [migrating push queues to Cloud Tasks documentation](https://cloud.google.com/appengine/docs/standard/python/taskqueue/push/migrating-push-queues) and [corresponding code samples](https://github.com/GoogleCloudPlatform/python-docs-samples/tree/master/appengine/standard/migration/taskqueue) and offer some additional benefits:
- Video content for those who prefer visual learning in addition to reading
- Codelab tutorials give hands-on experience and build "migration muscle-memory"
- More code samples gives developers a deeper understanding of migration steps

In short, these are the Step 5 codelabs/repos:
- Step 5a ([codelab](https://codelabs.developers.google.com/codelabs/cloud-gae-python-migrate-5a-gaetasksndb), [repo](/step5a-gae-ndb-tasks-py2)): Add push tasks (App Engine `taskqueue`) to Step 1 ([codelab](https://codelabs.developers.google.com/codelabs/cloud-gae-python-migrate-1-flask), [repo](/step1-flask-gaendb-py2)) Flask &amp; `ndb` Python 2 app
- Step 5b ([codelab](https://codelabs.developers.google.com/codelabs/cloud-gae-python-migrate-5b-cloudtasksndb), [repo](/step5b-cloud-ndb-tasks-py2)): Migrate from App Engine `ndb` &amp; `taskqueue` to Cloud NDB &amp; Cloud Tasks
- Step 5c ([codelab](https://codelabs.developers.google.com/codelabs/cloud-gae-python-migrate-5c-cloudtasksds), [repo](/step5c-cloud-ndb-tasks-py3)): Migrate Step 5b app to second-generation Python 3 App Engine &amp; Cloud Datastore

In *this* codelab/repo, participants start with the code in the (completed) [Step 5b repo](https://github.com/googlecodelabs/migrate-python-appengine-datastore/tree/master/step5b-cloud-ndb-tasks-py2) and port it from Python 2 to 3 at the same time migrating from Cloud NDB to Cloud Datatstore libraries. Because developer has ceased on Python 2.x, the Cloud client libraries are on newer 3.x versions than their 2.x counterparts.

This tutorial performs a pair of migrations from that Step 5a starting codebase:
- Migrate from Cloud NDB to Cloud Datastore
- Migrate from Python 2 to 3 and from first to second generation runtimes

NDB users will get an idea of how the Cloud Datastore client library differs, learn what changes they'll have to make to port their apps from 2.x to 3.x besides learning about the major differences between the first and second generation of App Engine runtimes.

If you haven't completed the [Step 5b codelab](https://codelabs.developers.google.com/codelabs/cloud-gae-python-migrate-5b-cloudtasks), we recommend you do so to familiarize yourself with its codebase as we start from there. (You can also just study the code in its repo linked above.)

---

## Migration

While this migration is partially advertised as Python 2 to 3, be aware that the sample at its core is already 2.x &amp; 3.x compatible, so there's very little Python that has to change. The majority of updates relate to the differences between the first and second generation App Engine runtimes.

The migration from Cloud NDB to Cloud Datastore is, for the most part, identical to that of the Step 3 ([codelab](http://codelabs.devsite.corp.google.com/codelabs/cloud-gae-python-migrate-3-datastore) and [2.x](https://github.com/googlecodelabs/migrate-python-appengine-datastore/tree/master/step3-flask-datastore-py2) or [3.x](https://github.com/googlecodelabs/migrate-python-appengine-datastore/tree/master/step3-flask-datastore-py3) repos). That migration is *not* covered here... those changes will "just happen". The focus areas include the Datastore changes in the task handler as well as updates in both the Cloud Datastore and Cloud Tasks client libraries (as the 2.x versions are effectively frozen). Review the Step 3 codelab if necessary to get clarity on how Cloud NDB differs from Cloud Datastore.

Here are the primary migration steps:

1. Update `requirements.txt`
1. Update `app.yaml`
1. Delete `appengine_config.py` and `lib` folder
1. Update application code

### Configuration

There are a few changes to `requirements.txt` from Step 5b, all related to Cloud client libraries. Replace `google-cloud-ndb` with `google-cloud-datastore` and add the `google-cloud-tasks` package.

At the time of this writing, Datastore is on 2.0.1 while Tasks is on 2.0.0. (The `requirements.txt` file in the repo will have the latest versions.) This differs from 2.x where `google-cloud-datastore` has been frozen at 1.15.3 while `google-cloud-tasks` is pinned at 1.5.0. Your `requirements.txt` will look something like this after those updates:

    Flask==1.1.2
    google-cloud-datastore==2.0.1
    google-cloud-tasks==2.0.0

The second generation App Engine runtime does not support [built-in third-party libraries like in 2.x](https://cloud.google.com/appengine/docs/standard/python/tools/built-in-libraries-27) nor does it support [bundling/vendoring of *non*-built-in libraries](https://cloud.google.com/appengine/docs/standard/python/tools/using-libraries-python-27#copying_a_third-party_library). The only requirement for third-party packages is to list them in `requirements.txt`. As a result, then entire `libraries` section of `app.yaml` can be deleted.

Also update to a Python 3 runtime, i.e., 3.7 or 3.8, and change all script handlers to `auto`. The second generation runtime requires web frameworks do their own routing, so they're not used in `app.yaml` any more. Your new, abbreviated `app.yaml` should look like this:

```yml
runtime: python38

handlers:
- url: /.*
  script: auto
```

An additional improvement you can make is to get rid of the `handlers:` section altogether (especially since `script: auto` is the only accepted directive regardless of URL path) and replace it with an `entrypoint:` directive. If you do *that*, your `app.yaml` will be even shorter (assuming `main.py` starts your service):

```yml
runtime: python38
entrypoint: python main.py
```

Check out these pages in the docs to learn more about the `entrypoint:` directive for `app.yaml` files:
- [Optional script handlers replaced by entrypoint](https://cloud.google.com/appengine/docs/standard/python3/config/appref#handlers_script)
- [The `entrypoint` reference](https://cloud.google.com/appengine/docs/standard/python3/config/appref#entrypoint)
- [Examples & best practices](https://cloud.google.com/appengine/docs/standard/python3/runtime#application_startup)
- [More examples & best practices](https://cloud.google.com/appengine/docs/flexible/python/runtime#application_startup)

Shortening `app.yaml` is optional but allows for easier containerization of your app (see Step 4 [codelab](https://codelabs.developers.google.com/codelabs/cloud-gae-python-migrate-4-cloudrun) and [2.x w/Docker](/step4-cloudndb-cloudrun-py2), [3.x w/Docker](/step4-cloudds-cloudrun-py3), or [3.x w/Cloud Buildpacks](/step4a-cloudrun-bldpks-py3) repos.


#### Delete `appengine_config.py` and `lib`

One of the welcome changes on the second generation of App Engine runtimes is that Bundling/vendoring of third-party packages is no longer required from users. No built-in libraries (per the changes to `app.yaml` above), no `appengine_config.py` file nor `lib` folder.


### Migrate from Cloud NDB &amp; Cloud Tasks 2.x to Cloud Datastore &amp; Cloud Tasks 3.x

#### Imports

The current app uses Cloud NDB which we'll shortly change to Cloud Datastore.

- BEFORE:

```python
from datetime import datetime
import json
import logging
import time
from flask import Flask, render_template, request
from google.cloud import ndb, tasks
```

Logging is simplified and enhanced in the second generation runtimes:
- For comprehensive logging experience, use [Cloud Logging](https://cloud.google.com/logging)
- For simple logging, just send to `stdout` (or `stderr`) via `print()`
- There's no need to use the Python `logging` module

As such, delete the import of `logging` and swap `google.cloud.ndb` with `google.cloud.datastore` so your `import` section now looks like this:

- AFTER:

```python
from datetime import datetime
import json
import time
from flask import Flask, render_template, request
from google.cloud import datastore, tasks
```

Similarly, switch to instantiating a Datastore client instead of an NDB client to talk to Datastore with:

```python
app = Flask(__name__)
ds_client = datastore.Client()
ts_client = tasks.CloudTasksClient()
```

#### Migrating to Cloud Tasks (and Cloud Datastore)

- BEFORE:

```python
class Visit(ndb.Model):
    visitor   = ndb.StringProperty()
    timestamp = ndb.DateTimeProperty(auto_now_add=True)

def store_visit(remote_addr, user_agent):
    'create new Visit entity in Datastore'
    with ds_client.context():
        Visit(visitor='{}: {}'.format(remote_addr, user_agent)).put()
```

As described in Step 3, Datastore does not have a data model class nor a way to automatically add a creation timestamp. It has more a JSON flavor to it, so delete the `Visit` class and replace `store_visit()` with the following:

- AFTER:

```python
def store_visit(remote_addr, user_agent):
    'create new Visit entity in Datastore'
    entity = datastore.Entity(key=ds_client.key('Visit'))
    entity.update({
        'timestamp': datetime.now(),
        'visitor': '{}: {}'.format(remote_addr, user_agent),
    })
    ds_client.put(entity)
```

The key function is `fetch_visits()`. Not only does it do the original query for the latest `Visit`s, but it also grabs the timestamp of the last `Visit` displayed and creates the push tasks that calls `/trim` (thus `trim()`) to mass-delete the old `Visit`s.

- BEFORE:

```python
def fetch_visits(limit):
    'get most recent visits & add task to delete older visits'
    with ds_client.context():
        data = Visit.query().order(-Visit.timestamp).fetch(limit)
    oldest = time.mktime(data[-1].timestamp.timetuple())
    oldest_str = time.ctime(oldest)
    logging.info('Delete entities older than %s' % oldest_str)
    task = {
        'app_engine_http_request': {
            'relative_uri': '/trim',
            'body': json.dumps({'oldest': oldest}).encode(),
            'headers': {
                'Content-Type': 'application/json',
            },
        }
    }
    ts_client.create_task(parent=QUEUE_PATH, task=task)
    return (v.to_dict() for v in data), oldest_str
```

The primary changes:
1. Swap out the Cloud NDB query for the Cloud Datastore equivalent; the query styles differ only slightly.
1. Datastore doesn't require use of a context manager nor does it make you extract its data (with `to_dict()`) like Cloud NDB does.
1. Replace logging calls with `print()`

After those changes, the code will look like this:

- AFTER:

```python
def fetch_visits(limit):
    'get most recent visits & add task to delete older visits'
    query = ds_client.query(kind='Visit')
    query.order = ['-timestamp']
    data = list(query.fetch(limit=limit))
    oldest = time.mktime(data[-1]['timestamp'].timetuple())
    oldest_str = time.ctime(oldest)
    print('Delete entities older than %s' % oldest_str)
    task = {
        'app_engine_http_request': {
            'relative_uri': '/trim',
            'body': json.dumps({'oldest': oldest}).encode(),
            'headers': {
                'Content-Type': 'application/json',
            },
        }
    }
    ts_client.create_task(parent=QUEUE_PATH, task=task)
    return data, oldest_str
```


#### Update (push) task handler

As you can see, the Cloud Tasks code stays the same. The final piece of code to look at is the task handler itself, `trim()`.

- BEFORE:

```python
@app.route('/trim', methods=['POST'])
def trim():
    '(push) task queue handler to delete oldest visits'
    oldest = float(request.get_json().get('oldest'))
    with ds_client.context():
        keys = Visit.query(
                Visit.timestamp < datetime.fromtimestamp(oldest)
        ).fetch(keys_only=True)
        nkeys = len(keys)
        if nkeys:
            logging.info('Deleting %d entities: %s' % (
                    nkeys, ', '.join(str(k.id()) for k in keys)))
            ndb.delete_multi(keys)
        else:
            logging.info('No entities older than: %s' % time.ctime(oldest))
    return ''   # need to return SOME string w/200
```

Like `fetch_visits()`, the bulk of the changes involve swapping out Cloud NDB code for Cloud Datastore's with just a tweak in query styles, and changing the logging calls to `print()`.

- AFTER:

```python
@app.route('/trim', methods=['POST'])
def trim():
    '(push) task queue handler to delete oldest visits'
    oldest = float(request.get_json().get('oldest'))
    query = ds_client.query(kind='Visit')
    query.add_filter('timestamp', '<', datetime.fromtimestamp(oldest))
    query.keys_only()
    keys = list(visit.key for visit in query.fetch())
    nkeys = len(keys)
    if nkeys:
        print('Deleting %d entities: %s' % (
                nkeys, ', '.join(str(k.id) for k in keys)))
        ds_client.delete_multi(keys)
    else:
        print('No entities older than: %s' % time.ctime(oldest))
    return ''   # need to return SOME string w/200
```

The subtle updates you may have missed in the code:
- Cloud NDB's queries allows for a keys-only data fetch:
    - `keys = Visit.query().fetch(keys_only=True)`
- Cloud Datastore queries always send back entities, so extracting the keys are required:
    - `keys = list(visit.key for visit in query.fetch())`
- Cloud NDB key IDs have a getter method:
    - `logging.info('Deleting %d entities: %s' % (nkeys, ', '.join(str(k.id()) for k in keys)))`
- Cloud Datastore key IDs are a property:
    - `print('Deleting %d entities: %s' % (nkeys, ', '.join(str(k.id) for k in keys)))`


#### Web template

There are no changes to `templates/index.html`.


## Next

Deploy to App Engine and confirm everything still works. This concludes the 3-party push task queue migration set of codelabs and matching repos.
