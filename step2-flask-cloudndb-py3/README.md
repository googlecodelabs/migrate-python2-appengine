# Step 2 (EXTRA) - After migrating to Google Cloud NDB, port to Python 3

## Introduction

We recommend developers migrate to Python 3 to access the latest App Engine runtimes & features. Developers can make this migration as soon as they've migrated to Cloud NDB (now). However since this can be a large undertaking, you can move to Py3 after any of the datastore migration steps, not just this one. One of the outstanding features of the App Engine second generation runtimes (Gen2) is that neither "vendored" nor bundled 3rd-party packages are required to be uploaded to the service. They are automatically installed directly from `requirements.txt`.

---

## Migration

Porting from Python 2 to 3 is not within the scope of this tutorial, and our simple sample app is already 2-3 compatible, so the only changes required are in configuration:

1. Simplify `app.yaml` to reference Python 3 and remove reference to bundled 3rd-party libraries.
1. Delete `appengine_config.py` as it's no longer necessary.
1. Delete the `lib` folder for the same reason.
1. Migrate from App Engine NDB to Cloud NDB

In addition to *actually* porting your app from Python 2.x to 3.x, you would also be migrating from the original App Engine runtime ("Gen1") to the next-gen runtime ("Gen2"), and there are some important differences you need to know which are [listed here](https://cloud.google.com/appengine/docs/standard/python3/python-differences).

### Configuration

#### Simplify `app.yaml`

The only real change for this sample app is to significantly shorten `app.yaml` down to just these lines for the runtime as well as routing:

```yml
runtime: python38

handlers:
- url: /.*
  script: auto
```

An additional improvement you can make is to get rid of the `handlers:` section altogether (especially since `script: auto` is the only accepted directive regardless of URL path) and replace it with an `entrypoint:` directive. In Gen1, handlers were necessary to help route requests to your app, but Gen2 requires routing be done by the web framework, not as an App Engine configuration.

If you do that, you're `app.yaml` may look like the following (assuming there is a "main" function in your `main.py` which we not have in ours until Step 4):

```yml
runtime: python38
entrypoint: python main.py
```

Check out [this page in the documentation](https://cloud.google.com/appengine/docs/standard/python3/runtime#application_startup) to find out more about the `entrypoint:` directive for `app.yaml` files.


#### Delete `appengine_config.py` and `lib`

One of the welcome changes on the second generation of App Engine runtimes is that Bundling/vendoring of third-party packages is no longer required from users. No built-in libraries (per the changes to `app.yaml` above), no `appengine_config.py` file nor `lib` folder.

Delete the `appengine_config.py` file and `lib` folder now. The `requirements.txt` and `templates/index.html` files remain unchanged.

---

## Next

From here, your options are:

- [**Step 4:**](/step4-cloudds-cloudrun-py3) Migrate your app to a container executing serverlessly on Cloud Run
- [**Step 3:**](/step3-flask-datastore-py3) Further modernize Datastore access from Cloud NDB to the (official) Cloud Datastore library (how users *outside of* App Engine access Cloud Datastore)
