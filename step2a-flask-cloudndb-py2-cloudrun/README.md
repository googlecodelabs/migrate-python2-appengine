# Step 2 (EXTRA) - Migrate from App Engine NDB to Google Cloud NDB and port to Cloud Run

## Introduction

This tutorial is for users who have migrated to Cloud NDB and wish to go straight to Cloud Run. The steps include replacing the configuration files and specifying how your app should start. Since you won't have App Engine's web server, you'll need to specify your own server or bundle one into your container. For testing and staging, it's easy to just run Flask's development server from Python, but developers can opt for something more powerful for production such as the [Cloud Run Quickstart sample](https://cloud.google.com/run/docs/quickstarts/build-and-deploy) which uses `gunicorn`.

---

## Migration

Learning how to use Cloud Run is not within the scope of this tutorial, so refer to the Quickstart above or the general [Cloud Run docs](https://cloud.google.com/run/docs). The sample app in this tutorial 1-2 more lines of code to support Flask's web server and swapping of configuration files to containerize it.

1. Delete `app.yaml` and `appengine_config.py` config files as they're not used in Cloud Run.
1. Delete the `lib` folder for the same reason
1. Add a `Dockerfile` with the container specifications and optionally a `.dockerignore` file as well.

### Configuration

The only configuration file needed is the `Dockerfile`, and this simple app only needs a few lines:

```Dockerfile
FROM python:3-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "main.py"]
```

Learn more about `Dockerfile` as well as `.dockerignore` from [this Cloud Run docs page](https://cloud.google.com/run/docs/quickstarts/build-and-deploy#containerizing).

The `requirements.txt` and HTML `templates/index.html` remain unchanged while the `app.yaml` and `appengine_config.py` files and `lib` folder are deleted.

### Start Flask web server

Cloud Run starts its web server on port 8080, automatically injected into the `PORT` environment variable. Add an `import os` at the top of `main.py` as well as a "main" at the bottom to start the server (if executed directly which our `Dockerfile` does):

```python
if __name__ == '__main__':
    app.run(debug=True, threaded=True, host='0.0.0.0',
            port=int(os.environ.get('PORT', 8080)))
```

---

## Summary

For the sample app in this tutorial, the overall contextual set of `diff`s (skipping this `README.md` and nonessential files) looks like this:

    $ diff -c step2*py2*
    Only in step2a-flask-cloudndb-py2-cloudrun: .dockerignore
    Only in step2a-flask-cloudndb-py2-cloudrun: Dockerfile
    Only in step2-flask-cloudndb-py2: app.yaml
    Only in step2-flask-cloudndb-py2: appengine_config.py
    diff -c step2-flask-cloudndb-py2/main.py step2a-flask-cloudndb-py2-cloudrun/main.py
    *** step2-flask-cloudndb-py2/main.py    2020-07-25 14:00:56.000000000 -0700
    --- step2a-flask-cloudndb-py2-cloudrun/main.py  2020-08-11 19:17:15.000000000 -0700
    ***************
    *** 1,3 ****
    --- 1,4 ----
    + import os
      from flask import Flask, render_template, request
      from google.cloud import ndb
      
    ***************
    *** 22,24 ****
    --- 23,29 ----
          store_visit(request.remote_addr, request.user_agent)
          visits = fetch_visits(10) or ()  # empty sequence if None
          return render_template('index.html', visits=visits)
    + 
    + if __name__ == '__main__':
    +     app.run(debug=True, threaded=True, host='0.0.0.0',
    +             port=int(os.environ.get('PORT', 8080)))
    Common subdirectories: step2-flask-cloudndb-py2/templates and step2a-flask-cloudndb-py2-cloudrun/templates

From here, you have some flexibility as to your next move. You can...

1. Port your app to Python 3 (no example provided, but use this example along with `step2-flask-cloudndb-py3`)
1. Further modernize Datastore access from Cloud NDB to the (official) Cloud Datastore library (how users access Cloud Datastore *outside of* App Engine) (no example provided but see this example along with `step3-flask-datastore-py2`)
