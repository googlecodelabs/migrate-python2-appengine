# Step 4 - Migrate from Google App Engine to Cloud Run (with Docker)

## Introduction

The next (but still optional) step of migrating from App Engine to an explicit container for [Cloud Run](https://cloud.google.com/run) offers several benefits:

- The ability to roll in functionality in any language, any library, any binary
- Opens the door to more product improvements only available to Cloud Run users
- Helps move even further away from vendor lock-in, dependency on Google Cloud
- Gives users the ability to more easily migrate their apps to VMs or Kubernetes, or move out of the cloud and run on-premise.

Regardless of whether you take this step, recognize your app is containerized anyway. If sticking with App Engine, the product hides all the container details from users so they don't need to think about containers. But those willing to trade-in some convenience for more flexibility can do so here.

---

## Background

App Engine existed before the concept of containers. Since Docker's launch, containers have become the de facto standard in packaging applications & dependencies into a single transportable & deployable unit. Users can imagine that App Engine apps were custom containers created by Google engineers, and the migration in this step help users move further away from vendor lock-in and continues the messaging of Google Cloud being an open platform to its customers and offering them more flexibility than ever before.

There are two options for users when migrating to a container, and it hinges upon what generation runtime your app is on as well as your [Docker](http://docker.com/) experience. Those on a newer runtime can use [Cloud Buildpacks](https://github.com/GoogleCloudPlatform/buildpacks) to containerize apps so they can be deployed to Cloud Run or other Google Cloud container platforms ([GCE](https://cloud.google.com/compute), [GKE](https://cloud.google.com/kubernetes-engine), [Anthos](http://cloud.google.com/anthos), etc.).

See Step 4a (see `step4a-flask-datastore-py3-cloudrun`) if interested in using Buildpacks over Docker. However, if you're on a first generation runtime or prefer to use Docker, you're in the right place.

---

## Migration

Containerizing your app for Cloud Run means no longer using App Engine. This means all App Engine configuration files will be replaced by Docker config files. You'll also have to tweak your code a bit to tell the container to launch the web server and start your app &mdash; these things were handled by App Engine automatically.

### Configuration

If you're on a first generation runtime like Python 2, you'll be replacing your `app.yaml` file with an equivalent `Dockerfile` specifying your container build.

1. Create a `Dockerfile` equivalent to `app.yaml`
1. Optionally add a `.dockerignore`
1. Delete (or backup)  `app.yaml`, `appengine_config.py`, and `lib` as they're no longer needed.

A minimal `Dockerfile` that works:

```Dockerfile
FROM python:2-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "main.py"]
```

A `.dockerignore` file can trim the size of your container and not bundle irrelevant files. The one we used:

```ignore
*.md
*.pyc
*.pyo
*.pyd
.git
__pycache__
```

### General configuration

Regardless of which technique you used to migrate to a container, below are changes common to both:

1. If you wish to use another web server, i.e., `gunicorn`, add it to `requirements.txt`, otherwise it should remain unchanged (to use the Flask development server).
1. App Engine automatically starts your application, but with Cloud Run you must provide an action for the `Dockerfile` `CMD` or `Procfile` directive.
1. Delete (or backup) `app.yaml`
1. `templates/index.html` should remain unchanged

Add a pair of lines at the bottom of `main.py` to start the application. Cloud Run automatically "injects" 8080 as the `PORT` environment variable, so you don't need to set it in `Dockerfile`:

```python
if __name__ == '__main__':
    app.run(debug=True, threaded=True, host='0.0.0.0',
            port=int(os.environ.get('PORT', 8080)))
```

---

## Next

The main `diff`s users will encounter:

1. New lines in `main.py`
1. Old App Engine configuration files deleted
1. A few new files (`Dockerfile`, `.dockerignore`) or (`service.yaml`, `Procfile` for Step 4a)

If you haven't migrated to Python 3, that's your only option here, as otherwise that concludes this tutorial.
