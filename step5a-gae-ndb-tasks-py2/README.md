# Step 5a - Add Push Tasks to App Engine `webapp2` &amp; `ndb` sample app

## Introduction

The goal of the Step 5 series of codelabs and repos like this is to help App Engine developers migrate from [Python 2 App Engine (Push) Task Queues](https://cloud.google.com/appengine/docs/standard/python/taskqueue/push) to [Google Cloud Tasks](https://cloud.google.com/tasks). They are meant to be *complementary* to the official [migrating push queues to Cloud Tasks documentation](https://cloud.google.com/appengine/docs/standard/python/taskqueue/push/migrating-push-queues) and [corresponding code samples](https://github.com/GoogleCloudPlatform/python-docs-samples/tree/master/appengine/standard/migration/taskqueue) and offer some additional benefits:
- Video content for those who prefer visual learning in addition to reading
- Codelab tutorials give hands-on experience and build "migration muscle-memory"
- More code samples gives developers a deeper understanding of migration steps

In this codelab/repo, participants start with the code in the (completed) [Step 1 repo](https://github.com/googlecodelabs/migrate-python-appengine-datastore/tree/master/step1-flask-gaendb-py2) where developers migrated to the Flask web framework and add support for Push Task Queues using the App Engine `taskqueue` API library. As you will recall, the sample app registers each visit (`GET` request to `/`) by creating a new `Visit` Entity for it then fetches and displays the 10 most recent `Visit`s in the web UI.

This codelab step adds a push task to delete all `Visit`s older than the oldest entry. If you haven't completed the [Step 1 codelab](https://codelabs.developers.google.com/codelabs/cloud-gae-python-migrate-1-flask), we recommend you do so to familiarize yourself with the Step 1 codebase.

---

## Augment sample with new feature

Rather than a migration, this step adds use of push Task Queues to the existing Step 1 app. The only modifications required are for the `main.py` application file and `templates/index.html` web template. The steps:

1. Add new Python `import`s
    - Add use of Python standard library date and time utilities
    - (optional but helpful) Add logging and function ["docstrings"](http://python.org/dev/peps/pep-0257/#id15)
1. Save timestamp of last (displayed) `Visit`
1. Add "delete old(est) entries" task
1. Display deletion message in web UI template

### Add new Python `import`s

It's useful to add logging to applications to give the developer (and the user) more information (as long as it's useful). For Python 2 App Engine, this is done by using the Python standard library `logging` module. For date &amp; time functionality, add use of the `datetime.datetime` class as well as the `time` module.

- BEFORE:

```python
from flask import Flask, render_template, request
from google.appengine.ext import ndb
```

The Python best practices of alphabetized group listing order:
1. Standard library modules first
1. Third-party globally-installed packages
1. Locally-installed packages
1. Application imports

Following that recommendation, your imports should look like this when done:

- AFTER:

```python
import logging
from datetime import datetime
import time
from flask import Flask, render_template, request
from google.appengine.api import taskqueue
from google.appengine.ext import ndb
```

### Save timestamp of last (displayed) `Visit`

The `fetch_visits()` function queries for the most recent visits. Add code to save the timestamp of the last `Visit`.

- BEFORE:

```python
def fetch_visits(limit):
    return (v.to_dict() for v in Visit.query().order(
            -Visit.timestamp).fetch(limit))
```

Instead of immediately returning all `Visit`s, we need to save the results, grab the last `Visit` and save its timestamp, both as a `str`ing (to display) and `float` (to send to the task).

- AFTER:

```python
def fetch_visits(limit):
    'get most recent visits & add task to delete older visits'
    data = Visit.query().order(-Visit.timestamp).fetch(limit)
    oldest = time.mktime(data[-1].timestamp.timetuple())
    oldest_str = time.ctime(oldest)
    logging.info('Delete entities older than %s' % oldest_str)
    taskqueue.add(url='/trim', params={'oldest': oldest})
    return (v.to_dict() for v in data), oldest_str
```

The `data` variable holds the `Visit`s previously returned immediately, and `oldest` is the timestamp of the oldest displayed `Visit` in seconds (as a `float`) since the epoch, retrieved by (extracting `datetime` object, morphed to Python [time 9-tuple normalized form](https://docs.python.org/library/time), then converted to `float`). A string version is also created for display purposes. A new push task is added, calling the handler (`/trim`) with `oldest` as its only parameter.

The same payload as the Step 1 `fetch_visits()` is returned to the caller in addition to `oldest` as a string. Following good practices, a function docstring was added (first unassigned string) along with an application log at the `INFO` level via `logging.info()`.

### Add "delete old(est) entries" task

While deletion of old `Visit`s could've easily been accomplished in `fetch_visits()`, this was a great excuse to make it a task which is handled asynchronously after `fetch_user()` returns, and the data is presented to the user. This improves the user experience because there is no delay in waiting for the deletion of the older Datastore entities to complete.

```python
@app.route('/trim', methods=['POST'])
def trim():
    '(push) task queue handler to delete oldest visits'
    oldest = request.form.get('oldest', type=float)
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

Push tasks are `POST`ed to the handler, so that must be specified (default: `GET`). Once the timestamp of the `oldest` visit is decoded, a Datastore query to find all entities strictly older than its timestamp is created. None of the actual data is needed, so a faster "keys-only" query is used. The number of entities to delete is logged, and the deletion command (`ndb.delete_multi()`) given. Logging also occurs if there are no entities to delete. A return value is necessary to go along with the HTTP 200 return code, so use an empty string to be efficient.


### Display deletion message in web UI template

It's also a good practice to have "docstrings" to document functionality, so add those as well. Add the following snippet after the unnumbered list of `Visit`s but before the closing `</body>` tag:

```html+jinja
{% if oldest %}
    <b>Deleting visits older than:</b> {{ oldest }}</p>
{% endif %}
```

### Configuration

There are no changes to any of the configuration (`app.yaml`, `appengine_config.py`, `requirements.txt`) files.

---

## Next

Try the app in the local development server (`dev_appserver.py app.yaml`), debug (if nec.), and deploy to App Engine and confirm everything still works. Once you're satisfied, move onto the next step:

- [**Step 5b:**](/step5b-cloud-ndb-tasks-py2) Migrate your app away from App Engine built-in libraries like `ndb` &amp; `taskqueue` to Cloud NDB &amp; Cloud Tasks
