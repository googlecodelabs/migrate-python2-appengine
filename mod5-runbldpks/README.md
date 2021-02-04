# Step 4a (EXTRA) - Migrate from Google App Engine to Cloud Run (with Cloud Buildpacks)

## Introduction

This codelab represents an alternative to Step 4 (just the Python 3 version) where you're migrating your App Engine app to Cloud Run, but using Cloud Buildpacks instead of Docker. As Docker is an industry standard for containers, users choosing to follow this path are those who don't want to have to become familiar with working with Docker product or carefully curating their `Dockerfile` and instead, opting for a more standardized approach to container-building that has multiple supporters in industry (more below).

---

## Background

App Engine existed before the concept of containers. Since Docker's launch, containers have become the de facto standard in packaging applications & dependencies into a single transportable & deployable unit. Users can imagine that App Engine apps were custom containers created by Google engineers, and the migration in this step help users move further away from vendor lock-in and continues the messaging of Google Cloud being an open platform to its customers and offering them more flexibility than ever before.

The alternative is [Cloud Buildpacks](https://github.com/GoogleCloudPlatform/buildpacks), a Google Cloud derivative of [CNCF Buildpacks](https://buildpacks.io/). Buildpacks originated in 2011 by Heroku and have since been adopted by Google Cloud and other cloud vendors, eventually forming the [CNCF industry consortium](https://www.cncf.io/about/members/) in 2018. Cloud Buildpacks containerizes apps so they can be deployed to Cloud Run or other Google Cloud container platforms ([GCE](https://cloud.google.com/compute), [GKE](https://cloud.google.com/kubernetes-engine), [Anthos](http://cloud.google.com/anthos), etc.) or other cloud container services as they're compatible with CNCF Buildpacks.

---

## Migration

While Docker is an industry standard, some developers may prefer to avoid learning yet another technology. An alternative exists for apps on one of the latest App Engine runtimes such as Python 3 can use Buildpacks and [this `app.yaml` tool](http://googlecloudplatform.github.io/app-engine-cloud-run-converter) to create a mostly-equivalent `service.yaml` that starts the service on Cloud Run. This technique also allows users to implement [continuous deployment](https://cloud.google.com/run/docs/continuous-deployment-with-cloud-build) (CD) from Git via [Cloud Build](https://cloud.google.com/cloud-build) as well as avoid creating a `Dockerfile` or knowing much about Docker.

### Configuration

1. Convert your `app.yaml` to a `service.yaml` with [the tool](http://googlecloudplatform.github.io/app-engine-cloud-run-converter).
1. Update `service.yaml` with your `PROJECT_ID`, `REGION`, `CONT_NAME`, and `SVC_NAME`.
1. Run the appropriate `gcloud` commands to build the container (see below).
1. Create a [`Procfile`](https://devcenter.heroku.com/articles/procfile) specifying the entrypoint of your app; see [example](https://devcenter.heroku.com/articles/getting-started-with-python#define-a-procfile).

Since this is only for Gen2 runtimes, we have to paste the contents of `step3-flask-datastore-py3/app.yaml` into the tool, which generates a `service.yaml` that looks like this:

```yml
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: SVC_NAME
  labels:
    migrated-from: app-engine
    cloud.googleapis.com/location: REGION
spec:
  template:
    metadata:
      annotations: {}
    spec:
      containers:
        - image: gcr.io/PROJECT_ID/IMG_NAME
      serviceAccountName: PROJECT_NUM-compute@developer.gserviceaccount.com
```

Update the image and service account name, then run one of these build commands, depending on whether your service is public (or not):
    - Run `gcloud alpha builds submit --pack image=gcr.io/PROJECT_ID/IMG_NAME && gcloud beta run services replace service.yaml --region us-central1 --platform managed` (private services)
    - OR `gcloud run services add-iam-policy-binding my-service --member="allUsers" --role="roles/run.invoker" --region us-central1 --platform managed` (public services)

Delete the `app.yaml` (or back it up somewhere) as it is no longer needed. Then create a `Procfile` file specifying the application entry-point. The one for this app:

```yml
web: python main.py
```

More on configuration below covering updates to our application regardless of which migration technique is employed.

### General configuration

Regardless of which technique you used to migrate to a container, below are changes common to both:

1. If you wish to use another web server, i.e., `gunicorn`, add it to `requirements.txt`, otherwise it should remain unchanged (to use the Flask development server).
1. App Engine automatically starts your application, but with Cloud Run you must provide an action for the `Dockerfile` `CMD` or `Procfile` directive.
1. Delete (or backup) `app.yaml`
1. `templates/index.html` should remain unchanged

Add a pair of lines at the bottom of `main.py` to start the application. Cloud Run automatically "injects" 8080 as the `PORT` environment variable, so you don't need to set it in a config file:

```python
if __name__ == '__main__':
    app.run(debug=True, threaded=True, host='0.0.0.0',
            port=int(os.environ.get('PORT', 8080)))
```

---

## Next

Congratulations... this app is fully modernized now, concluding this tutorial. If you want to consider containerizing your app with Docker instead of Buildpacks, take a look at both Step 4 tutorials (see the [Python 2 Cloud NDB](/step4-cloudndb-cloudrun-py2) and [Python 3 Cloud Datastore](/step4-cloudds-cloudrun-py3) apps).
