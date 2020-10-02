# Python 2 App Engine app migration: data storage
### To modern datastores, Python 3, and Cloud Run containers

[Google App Engine](https://cloud.google.com/appengine) (standard) has undergone a number of product upgrades over the past few years, leaving some early adopters unable to easily move off the original platform. These codelabs (free, self-paced, hands-on tutorials) aim to help developers modernize their applications by experiencing individual migration steps via a sample application meant to model theirs.

## Prerequisites

- A Google account (G Suite accounts may require administrator approval)
- A Google Cloud Platform (GCP) project with an active billing account
- Familiarity with operating system terminal/shell commands
- General skills in [Python](http://python.org) 2 and/or 3
- Familiarity with the App Engine Python 2 runtime

The intended audiences of this tutorial and corresponding video content are Information Technology decision-makers (ITDMs) as well as technical practitioners tasked with investigating and/or carrying out these migrations.

## Cost

Use of GCP products & APIs is not free. While you may not have needed to enable billing with early App Engine applications, all applications now require an active billing account. App Engine's [pricing](https://cloud.google.com/appengine/pricing) and [quota](https://cloud.google.com/appengine/quotas) information should be referenced. App Engine and other GCP products have an ["Always Free" tier](https://cloud.google.com/free/docs/gcp-free-tier#always-free). Users only incur billing when these daily/monthly quotas are exceeded. The migration exercises in these tutorials should not incur any billing so long as you stay within the limits described above.

## Support for Python 2 &amp; 3

It's important to note that for App Engine (Standard), Python 2 is only supported as a first-generation ("Gen1") runtime whereas Python3 is only supported as a next generation ("Gen2") runtime. This means that porting application from Python 2 to 3 also means migrating from Gen1 to Gen2 where things are different.

The most notable changes for developers are that bundled App Engine built-in services are absent from Gen2. The Gen1 bundled services have "grown-up" to become standalone products or have been deprecated. Gen2 also expects web apps to perform their own application (not network) routing.

> **NOTE:** App Engine ([Flexible](https://cloud.google.com/appengine/docs/flexible/python/runtime?hl=en#interpreter)) is a Gen2 service but is not within the scope of these tutorials. Developers who are curious can compare App Engine [Standard vs. Flexible](https://cloud.google.com/appengine/docs/the-appengine-environments).

## Description

We present a very basic first-generation Python 2.7 App Engine app and walk developers through modernization migration steps where each is represented by a codelab and corresponding video. Some of the steps are more crucial while most steps are optional, depending on user needs & preference. Think of it as a train ride where passengers can "get off" at their desired stops or continue their onward journey.

The sample app does not address complexities in your apps but serves as a guide to give you an idea of what is required for each of the migrations. The baseline sample is a Python 2.7 (Gen1) app built on the `webapp2` micro web framework and uses the `ndb` App Engine Datastore library.

> **NOTE:**
> - If your app does not have a user interface, i.e., mobile backends, etc., you still need to migrate to the Flask (or another) web framework to handle mobile app requests. An alternative is to use Cloud Endpoints or migrate your app to the [Firebase mobile &amp; web app platform](https://firebase.google.com) where you can port your App Engine "API handlers" to [Cloud Functions for Firebase](https://firebase.google.com/products/functions).
> - Users interested in bringing back their dead apps that originally ran on the original Python 2.5 runtime ([deprecated in 2013](http://googleappengine.blogspot.com/2013/03/python-25-thanks-for-good-times.html) and [shutdown in 2017](https://cloud.google.com/appengine/docs/standard/python/python25) must [migrate from `db` to `ndb`](http://cloud.google.com/appengine/docs/standard/python/ndb/db_to_ndb) before attempting the techniques shown in this tutorial.

As mentioned above, some steps are more critical while others are *optional*. We recommend incremental updates. We designed each step to be relatively easy, so you experience each migration individually. However, there are some of you for whom the migration process may be easier where you may be able to take larger migration leaps.

We suggest considering where you want to end up eventually, playing with each migration step, then choose how you want to migrate your application then plan your path forward accordingly. For your app, determine how much migration you want to do, execute it, ensure all your unit tests & CI/CD work perfectly, and get to a stable place before taking the next step.

## Table of Contents

Each major migration step has its own codelab & corresponding overview video. The step numbers correspond to their own folders, and generally each have folders for Python 2 &amp; 3 ports. Some have an alternative or secondary succeeding migration—these end with "a", i.e., "Step 3a".

1. **Migrate from `webapp2` to [Flask](https://flask.palletsprojects.com/)**
    - Strongly recommended
    - Need to do this port regardless of whether you have a web UI
    - You can use another web framework as long as it supports routing
    - `webapp2` does not do routing so unsupported in Gen2 (meaning N/A in Python 3)
1. **Migrate from App Engine NDB to [Cloud NDB](https://googleapis.dev/python/python-ndb/latest)**
    - Also strongly recommended
    - More options available after completing this step
        - Can migrate from Python 2 to 3 after this step
        - Can migrate to Cloud Run after this step (Step 4)
    - Remaining datastore migration steps optional as Cloud NDB works in Python 2 &amp; 3
    - App Engine NDB N/A in Python 3, so must move to Cloud NDB to move to 3.x
1. **Migrate from Cloud NDB to [Cloud Datastore](http://cloud.google.com/datastore)**
    - Optional if you only have App Engine apps &amp; only using Cloud NDB
    - Only recommended if you're already using Cloud Datastore in other apps
        - "Other apps" means App Engine *and* non-App Engine) apps
        - Help make codebase more consistent with possibly reusable components
        - Help consistent &amp; reusable codebase may mean reduce maintenance costs
    - Can migrate to [Cloud Firestore](http://cloud.google.com/firestore) after this step (Step 3a)
        - Quite optional: infrequent/uncommon as it is "expensive"
            - Requires new project &amp; Datastore has better write performance
        - For those who **must have** Firestore Firebase features
1. **Migrate from App Engine to [Cloud Run](http://cloud.google.com/run)**
    - Migrate your app to a container with [Docker](http://docker.com)
    - Alternative container migration with [Cloud Buildpacks](https://github.com/GoogleCloudPlatform/buildpacks) (Step 4a)

## Summary

The table below summarizes each migration step and which options are available for developers after each step. Each step has a corresponding directory representing the state of the sample app after the previous migration step. The first step ("step0") represents the initial Python 2.7 App Engine app built using `ndb` and `webapp2`.

Python 2 | Next | Python 3 | Description
--- | --- | --- | ---
[`step0-webapp2-gaendb-py2`](/step0-webapp2-gaendb-py2) | &darr; | _N/A_ | Original GAE sample on GAE `ndb` & `webapp2`
[`step1-flask-gaendb-py2`](/step1-flask-gaendb-py2) | &darr; | _N/A_ | Migrate to Flask
[`step2-flask-cloudndb-py2`](/step2-flask-cloudndb-py2) | &darr; or &rarr; or &DownArrowBar;ª | [`step2-flask-cloudndb-py3`](/step2-flask-cloudndb-py3) | Migrate to Cloud NDB
[`step3-flask-datastore-py2`](/step3-flask-datastore-py2) | &darr; or &rarr; or &DownArrowBar;+º | [`step3-flask-datastore-py3`]('step3-flask-datastore-py3) | Migrate to Cloud Datastore
[ª`step4-cloudndb-cloudrun-py2`](/step4-cloudndb-cloudrun-py2) | &rarr; | [`step4-cloudds-cloudrun-py3`](/step4-cloudds-cloudrun-py3) | Migrate to Cloud Run (with Docker)

### Alternatives

- Cloud Datastore &amp; Cloud Firestore are mutually-exclusive, thus requiring a new project
    - Thus it is much less likely users perform this migration; see Step 3a if it's a **must-have**
- Step 4a is for developers who want to containerize their apps but **without** Docker
    - Users either don't want to learn it nor curate a Dockerfile.
- Both alternatives are only available in Python 3;  users can extrapolate for Python 2

Python 2 | Next | Python 3 | Description
--- | --- | --- | ---
_N/A_ | _N/A_ | º[`step3a-flask-firestore-py3`](/step3a-flask-firestore-py3) | Migrate to Cloud Firestore (uncommon; see above)
_N/A_ | _N/A_ | +[`step4a-cloudrun-bldpks-py3`](/step4a-cloudrun-bldpks-py3) | Migrate to Cloud Run (with Cloud Buildpacks)

### Canonical code samples

- These sample app code samples were made specifically for the corresponding codelabs &amp; videos.
- The canonical migration code samples are those in the [official migration documentation](https://cloud.google.com/appengine/docs/standard/python/migrate-to-python3)
- [Canonical migration code samples repo](https://github.com/GoogleCloudPlatform/python-docs-samples/tree/master/appengine/standard/migration)
    - Example: [GAE NDB to Cloud NDB migration sample](https://github.com/GoogleCloudPlatform/python-docs-samples/tree/master/appengine/standard/migration/ndb/overview)

## Next

- [**Step 0:**](/step0-webapp2-gaendb-py2) Take a look at the original Python 2.7 App Engine NDB Datastore `webapp2` app source code.
- [**Step 1:**](/step1-flask-gaendb-py2) Take the first tutorial and migrate away from `webapp2` to Flask.

## References

- App Engine Migration
    - [Migrate from GAE Gen1 to Gen2 (Python 2 to 3)](http://cloud.google.com/appengine/docs/standard/python/migrate-to-python3)
    - [Migrate from App Engine NDB to Cloud NDB](http://cloud.google.com/appengine/docs/standard/python/migrate-to-python3/migrate-to-cloud-ndb) (Step 2)
    - [App Engine NDB to Cloud NDB official sample app](https://github.com/GoogleCloudPlatform/python-docs-samples/tree/master/appengine/standard/migration/ndb/overview) (Step 2)
    - [App Engine `app.yaml` to Cloud Run `service.yaml` tool](http://googlecloudplatform.github.io/app-engine-cloud-run-converter) (Step 4a)
    - [Migrate from App Engine `db` to `ndb`](http://cloud.google.com/appengine/docs/standard/python/ndb/db_to_ndb) (Step -1 [before Step 0]; only for reviving "dead" Python 2.5 apps)

- Python App Engine
    - [Python 2 App Engine (Standard; Gen1)](https://cloud.google.com/appengine/docs/standard/python/runtime)
    - [Python 3 App Engine (Standard; Gen2)](https://cloud.google.com/appengine/docs/standard/python3/runtime)
    - [Python App Engine (Flexible; Gen2)](https://cloud.google.com/appengine/docs/flexible/python)

- Google Cloud Platform (GCP)
    - [Python on GCP](https://cloud.google.com/python)
    - [Cloud client libraries](https://cloud.google.com/apis/docs/cloud-client-libraries)
    - [All GCP documentation](https://cloud.google.com/docs)
