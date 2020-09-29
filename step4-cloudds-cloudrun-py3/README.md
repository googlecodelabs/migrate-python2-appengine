# Step 4 - Migrate from Python 3 App Engine with Cloud Datastore to Cloud Run (with Docker)

## Introduction

The next (but still optional) step of migrating from App Engine to an explicit container for [Cloud Run](https://cloud.google.com/run) offers several benefits:

- The ability to roll in functionality in any language, any library, any binary
- Opens the door to more product improvements only available to Cloud Run users
- Helps move even further away from vendor lock-in, dependency on Google Cloud
- Gives users the ability to more easily migrate their apps to VMs or Kubernetes, or move out of the cloud and run on-premise.

This migration is slightly different from its Python 2 twin (the "other" Step 4) in that we're using Cloud Datastore for this 3.x version but Cloud NDB for the 2.x version. If you're ready for containerization, this tutorial show you how to migrate Python 3 App Engine apps using Cloud Datastore to Cloud Run.

The steps include replacing the configuration files and specifying how your app should start. Since you won't have App Engine's web server, you'll need to specify your own server or bundle one into your container. For testing and staging, it's easy to just run Flask's development server from Python, but developers can opt for something more powerful for production such as the [Cloud Run Quickstart sample](https://cloud.google.com/run/docs/quickstarts/build-and-deploy) which uses `gunicorn`.

---

## Background

App Engine existed before the concept of containers. Since Docker's launch, containers have become the de facto standard in packaging applications & dependencies into a single transportable & deployable unit. Users can imagine that App Engine apps were custom containers created by Google engineers, and the migration in this step help users move further away from vendor lock-in and continues the messaging of Google Cloud being an open platform to its customers and offering them more flexibility than ever before.

There are two options for users when migrating to a container, and it hinges upon what generation runtime your app is on as well as your [Docker](http://docker.com/) experience. Those on a newer runtime can use [Cloud Buildpacks](https://github.com/GoogleCloudPlatform/buildpacks) to containerize apps so they can be deployed to Cloud Run or other Google Cloud container platforms ([GCE](https://cloud.google.com/compute), [GKE](https://cloud.google.com/kubernetes-engine), [Anthos](http://cloud.google.com/anthos), etc.).

See Step 4a (see `step4a-cloudrun-bldpks-py3`) if interested in using Buildpacks over Docker. However, if you're on a first generation runtime or prefer to use Docker, you're in the right place.

---

## Migration

Learning how to use Cloud Run is not within the scope of this tutorial, so refer to the Quickstart above or the general [Cloud Run docs](https://cloud.google.com/run/docs). Containerizing your app for Cloud Run means no longer using App Engine. This means all App Engine configuration files will be replaced by Docker config files. You'll also have to tweak your code a bit to tell the container to launch the web server and start your app &mdash; these things were originally handled by App Engine automatically.

1. Delete `app.yaml` and `appengine_config.py` config files as they're not used with Cloud Run.
1. Delete the `lib` folder for the same reason.
1. Add a `Dockerfile` with the container specifications and optionally a `.dockerignore` file as well.
1. The `requirements.txt` and `templates/index.html` are fine to leave as-is.
1. Modify `main.py` to start up the Flask app.

### Configuration

The only configuration file needed is the [`Dockerfile`](https://docs.docker.com/develop/develop-images/dockerfile_best-practices) that outlines how to build &amp; run the container. This simple app only needs a minimal `Dockerfile`; here's one that works:

```Dockerfile
FROM python:3-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "main.py"]
```

App Engine automatically starts your application, but Cloud Run doesn't. This is what the `Dockerfile` `ENTRYPOINT`  directive is for. An alternative is to put a similar directive in a [`Procfile`](https://devcenter.heroku.com/articles/procfile). Our `ENTRYPOINT` launches `python` to execute `main.py` to start the Flask development server. You may also use a production web server like `gunicorn` if desired, and if so, be sure to add it to `requirements.txt`. Learn more about `Dockerfile` as well as `.dockerignore` from [this Cloud Run docs page](https://cloud.google.com/run/docs/quickstarts/build-and-deploy#containerizing) as well as see an example `Dockerfile` that spawns `gunicorn`.

Optionally add a `.dockerignore`, or if you already have one, it should remain as-is. A `.dockerignore` file can trim the size of your container and not bundle irrelevant files. The one we used:

```ignore
*.md
*.pyc
*.pyo
.git/
.gitignore
__pycache__
```

Add a pair of lines at the bottom of `main.py` to start the application. Cloud Run automatically "injects" 8080 as the `PORT` environment variable, so you don't need to set it in `Dockerfile`:

Cloud Run starts its web server on port 8080, automatically injected into the `PORT` environment variable. Add an `import os` at the top of `main.py` as well as a "main" at the bottom to start the server (if executed directly which our `Dockerfile` does):

```python
if __name__ == '__main__':
    app.run(debug=True, threaded=True, host='0.0.0.0',
            port=int(os.environ.get('PORT', 8080)))
```

Doublecheck there are no files/folders named, `app.yaml`, `appengine_config.py`, nor `lib`, and that `requirements.txt` and `templates/index.html` are the same as before unless you added a production web server like `gunicorn` to your `requirements.txt'.

---

## Next

Congratulations... your app is fully modernized now, concluding this tutorial. From here, there is only one more thing you can investigate:

- [**Step 4a:**](/step4a-cloudrun-bldpks-py3) An alternative to app in *this* tutorial, containerizing your app with [Cloud Buildpacks](https://github.com/GoogleCloudPlatform/buildpacks) instead of Docker.
