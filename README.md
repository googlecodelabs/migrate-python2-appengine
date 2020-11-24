# Python 2 App Engine app migration
### To modern runtime, Cloud services, Python 3, and Cloud Run containers

[Google App Engine](https://cloud.google.com/appengine) (standard) has undergone a number of product upgrades over the past few years, leaving some early adopters unable to easily move off the original platform. This repo supports various migration codelabs (free, self-paced, hands-on tutorials) aim to give developers hands-on experience and develop muscle memory in doing individual migrations so they can modernize their applications. This is done via a sample application meant to model basic elements found in existing first-generation apps and applying individual migration steps to each.

## Prerequisites

- A Google account (G Suite accounts may require administrator approval)
- A Google Cloud Platform (GCP) project with an active billing account
- Familiarity with operating system terminal/shell commands
- General skills in [Python](http://python.org) 2 and/or 3
- Familiarity with the App Engine Python 2 runtime

The intended audiences of this tutorial and corresponding video content are Software Engineers, Information Technology decision-makers (ITDMs) as well as other technical practitioners tasked with investigating and/or carrying out such migrations.

## Cost

Use of GCP products & APIs is not free. While you may not have needed to enable billing with early App Engine applications, all applications now require an active billing account. App Engine's [pricing](https://cloud.google.com/appengine/pricing) and [quota](https://cloud.google.com/appengine/quotas) information should be referenced. App Engine and other GCP products have an ["Always Free" tier](https://cloud.google.com/free/docs/gcp-free-tier#always-free). Users only incur billing when these daily/monthly quotas are exceeded. The migration exercises in these tutorials should not incur any billing so long as you stay within the limits described above.

## Support for Python 2 &amp; 3

It's important to note that for App Engine (Standard), Python 2 is only supported as a 1st generation ("Gen1") runtime whereas Python 3 is only supported by the 2nd generation ("Gen2") runtime. This means that porting application from Python 2 to 3 also means migrating from Gen1 to Gen2 where things are different. (Python 2 belongs in the same class as Java 6-8, PHP 5, and Go 1.8-1.11 first-gen apps.) See the exact differences on the [App Engine runtime documentation page](https://cloud.google.com/appengine/docs/standard/runtimes). One key change: bundled App Engine built-in services are absent from Gen2 (they have either matured to become standalone products or have been deprecated). The other key change: you must use web frameworks that do their own routing.

> **NOTE:** App Engine ([Flexible](https://cloud.google.com/appengine/docs/flexible/python/runtime?hl=en#interpreter)) is a Gen2 service but is not within the scope of these tutorials. Developers who are curious can compare App Engine [Standard vs. Flexible](https://cloud.google.com/appengine/docs/the-appengine-environments).

## Description

Each folder represents a single migration step, and the plan is to have a corresponding code repo and developer video as well. It all starts with a basic Gen1 Python 2.7 app then makes the minimum "required" migrations away from built-in App Engine services such as `webapp2` micro web framework and the `ndb` Datastore library. These comprise the [Step 0](/step0-webapp2-gaendb-py2) 2.7 app.

## Table of Contents

Each major migration step has its own codelab & corresponding overview video. The step numbers correspond to their own folders, and generally each have folders for Python 2 &amp; 3 ports. Some have an alternative or secondary succeeding migration—these end with "a", i.e., "Step 3a".

1. **Migrate from `webapp2` to [Flask](https://flask.palletsprojects.com/)** ([2.x-only](/step1-flask-gaendb-py2))
    - Required/strongly recommended
    - Can select another web framework as long as it supports routing
    - `webapp2` [exists for 3.x](https://github.com/fili/webapp2-gae-python37) but does not do routing thus unsupported by App Engine
1. **Migrate from App Engine NDB to [Cloud NDB](https://googleapis.dev/python/python-ndb/latest)** ([2.x](/step2-flask-cloudndb-py2) or [3.x](/step2-flask-cloudndb-py3))
    - Required/strongly recommended (`ndb` does not support 3.x)
    - More options available after completing this step
        - Can port to 3.x after this step (Cloud NDB Python 2 &amp; 3-compatible)
        - Can migrate to Cloud Run after this step (Step 4 below)
    - No additional Datastore migrations required
1. **Migrate from Cloud NDB to [Cloud Datastore](http://cloud.google.com/datastore)** ([2.x](/step3-flask-datastore-py2) or [3.x](/step3-flask-datastore-py3))
    - Only recommended if using Cloud Datastore elsewhere (GAE *and* non-App Engine) apps
        - Helps w/code consistency &amp; reusability, reduces maintenance costs
    - Can migrate to [Cloud Firestore](http://cloud.google.com/firestore) after this step ([Step 3a](/step3a-flask-firestore-py2); 3.x-only)
        - **Very** optional: infrequent/uncommon &amp; "expensive" migration
            - Requires new project &amp; Datastore has better write performance (currently)
            - If you **must have** Firestore's Firebase features
1. **Migrate from App Engine to [Cloud Run](http://cloud.google.com/run)**
    - "Containerize" your app (migrate your app to a container) with...
    - [Docker](http://docker.com) ([2.x w/Cloud NDB](/step4-cloudndb-cloudrun-py2) or [3.x w/Cloud Datastore](/step4-cloudds-cloudrun-py3))
    - Cloud Buildpacks ([Step 4a](/step4-cloudrun-bldpks-py3)) ; 3.x-only w/Cloud Datastore)

Think of it as a train ride where the first pair of stops are required, then the passengers can "get off" at any upcoming station or continue their onward journey.

### Considerations for mobile developers
If your original app users does *not* have a user interface, i.e., mobile backends, etc., but still uses `webapp2` for routing, some migration must still be completed. Your options:
- Migrate to Flask (or another) web framework but keep app on App Engine
- Use Cloud Endpoints for your mobile endpoints
- Break-up your monolithic app to "microservices" and migrate your app to either:
    - Google Cloud Functions](https://cloud.google.com/functions)
    - [Firebase mobile &amp; web app platform](https://firebase.google.com) (and [Cloud Functions for Firebase](https://firebase.google.com/products/functions) [customized for Firebase])

> **NOTE:**
Long-time users wishing to bring back apps on the inaugural Python 2.5 runtime, [deprecated in 2013](http://googleappengine.blogspot.com/2013/03/python-25-thanks-for-good-times.html) and [shutdown in 2017](https://cloud.google.com/appengine/docs/standard/python/python25), must [migrate from `db` to `ndb`](http://cloud.google.com/appengine/docs/standard/python/ndb/db_to_ndb) (and 2.5 to 2.7) before attempting these migrations.

## Summary

The table below summarizes each migration step and which options are available for developers after each step. Each step has a corresponding directory representing the state of the sample app after the previous migration step. The first step ("step0") represents the initial Python 2.7 App Engine app built using `ndb` and `webapp2`.

Python 2 | Next | Python 3 | Description
--- | --- | --- | ---
[`step0-webapp2-gaendb-py2`](/step0-webapp2-gaendb-py2) | &darr; | _N/A_ | Original GAE sample on GAE `ndb` & `webapp2`
[`step1-flask-gaendb-py2`](/step1-flask-gaendb-py2) | &darr; | _N/A_ | Migrate to Flask
[`step2-flask-cloudndb-py2`](/step2-flask-cloudndb-py2) | &darr; or &rarr; or &DownArrowBar;ª | [`step2-flask-cloudndb-py3`](/step2-flask-cloudndb-py3) | Migrate to Cloud NDB
[`step3-flask-datastore-py2`](/step3-flask-datastore-py2) | &darr; or &rarr; or &DownArrowBar;+º | [`step3-flask-datastore-py3`](/step3-flask-datastore-py3) | Migrate to Cloud Datastore
_N/A_ | _N/A_ | º[`step3a-flask-firestore-py3`](/step3a-flask-firestore-py3) | Migrate to Cloud Firestore (uncommon; see above)
[ª`step4-cloudndb-cloudrun-py2`](/step4-cloudndb-cloudrun-py2) | &rarr; | [`step4-cloudds-cloudrun-py3`](/step4-cloudds-cloudrun-py3) | Migrate to Cloud Run (with Docker)
_N/A_ | _N/A_ | +[`step4a-cloudrun-bldpks-py3`](/step4a-cloudrun-bldpks-py3) | Migrate to Cloud Run (with Cloud Buildpacks)

### Canonical code samples

- This repo, along with corresponding codelabs &amp; videos are complementary to the official docs &amp; code samples.
    - The [official Python 2 to 3 migration documentation](https://cloud.google.com/appengine/docs/standard/python/migrate-to-python3)
    - [Canonical migration code samples repo](https://github.com/GoogleCloudPlatform/python-docs-samples/tree/master/appengine/standard/migration)
        - Example: [GAE NDB to Cloud NDB](https://github.com/GoogleCloudPlatform/python-docs-samples/tree/master/appengine/standard/migration/ndb/overview)

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
