# Python 2 App Engine app migration: data storage
### To modern datastores, Python 3, and Cloud Run containers

[Google App Engine](https://cloud.google.com/appengine) (standard) has undergone a number of product upgrades over the past few years, leaving some early adopters unable to easily move off the original platform. These codelabs (free, self-paced, hands-on tutorials) aim to help developers modernize their applications by experiencing individual migration steps via a sample application meant to model theirs.

## Prerequisites

- A Google account (G Suite accounts may require administrator approval)
- A Google Cloud Platform project with an active billing account
- Familiarity with operating system terminal/shell commands
- General skills in [Python](http://python.org) 2 and/or 3
- Familiarity with the App Engine Python 2 runtime

The intended audiences of this tutorial and corresponding video content are Information Technology decision-makers (ITDMs) as well as technical practitioners tasked with investigating and/or carrying out these migrations.

## Cost

Use of Google Cloud Platform (GCP) products & APIs is not free. While you may not have needed to enable billing with early App Engine applications, all applications now require an active billing account. App Engine's [pricing](https://cloud.google.com/appengine/pricing) and [quota](https://cloud.google.com/appengine/quotas) information should be referenced. App Engine and other GCP products have an ["Always Free" tier](https://cloud.google.com/free/docs/gcp-free-tier#always-free). Users only incur billing when these daily/monthly quotas are exceeded. The migration exercises in these tutorials should not incur any billing so long as you stay within the limits described above.

## Support for Python 2 &amp; 3

It's important to note that for App Engine (Standard), Python 2 is only supported as a first-generation ("Gen1") runtime whereas Python3 is only supported as a second-generation ("Gen2") runtime. This means that porting application from Python 2 to 3 also means migrating from Gen1 to Gen2 where things are different.

The most notable changes for developers are that bundled App Engine built-in services are absent from Gen2. The Gen1 bundled services have "grown-up" to become standalone products or have been deprecated. Gen2 also expects web apps to perform their own application (not network) routing.

> **NOTE:** App Engine ([Flexible](https://cloud.google.com/appengine/docs/flexible/python/runtime?hl=en#interpreter)) is a Gen2 service but is not within the scope of these tutorials. Developers who curious can compare App Engine [Standard vs. Flexible](https://cloud.google.com/appengine/docs/the-appengine-environments).

## Description

We present a very basic first-generation Python 2.7 App Engine app and walk developers through modernization migration steps where each is represented by a codelab and corresponding video. Some of the steps are more crucial while most steps are optional, depending on user needs & preference. Think of it as a train ride where passengers can "get off" at their desired stops or continue their onward journey.

The sample app does not address complexities in your apps but serves as a guide to give you an idea of what is required for each of the migrations. The baseline sample is a Python 2.7 (Gen1) app built on the `webapp2` micro web framework and uses the `ndb` App Engine Datastore library.

> **NOTE:**
> 1. It is also possible your app does not have a user interface, i.e., mobile backends, etc., so migrating the web framework (step 1) can be skipped.
> 1. Users interested in bringing back their dead apps that originally ran on the [deprecated Python 2.5 runtime](http://googleappengine.blogspot.com/2013/03/python-25-thanks-for-good-times.html) (shutdown in 2017) need to [migrate from `db` to `ndb`](http://cloud.google.com/appengine/docs/standard/python/ndb/db_to_ndb) before attempting the techniques shown in this tutorial.

As mentioned above, some steps are more critical while others are *optional*. We recommend incremental updates. We designed each step to be relatively easy, so you experience each migration individually. However, there are some of you for whom the migration process may be easier where you may be able to take larger migration leaps.

We suggest considering where you want to end up eventually, playing with each migration step, then choose how you want to migrate your application then plan your path forward accordingly. For your app, determine how much migration you want to do, execute it, ensure all your unit tests & CI/CD work perfectly, and get to a stable place before taking the next step.

## Table of Contents

Each of the migration steps have their own codelabs & corresponding overview videos:

1. Migrate from `webapp2` to Flask
    - Stongly recommended if you have a web UI
    - You can use another web framework as long as it supports routing
1. Migrate from App Engine NDB to Cloud NDB
    - Stongly recommended
    - Can migrate from Python 2 to 3 after this step
    - Can migrate directly to Cloud Run after this step (see Step "2a" below)
    - Remaining datastore migration steps optional
1. Migrate from Cloud NDB to Cloud Datastore
    - Cloud NDB works on both Python 2 & 3 App Engine runtimes (old & new), so it is optional
    - Recommended if already using Cloud Datastore in other (App Engine *and* non-App Engine) apps & want a consistent/reusable codebase plus reduce maintenance costs
    - If all you have are App Engine apps using Cloud NDB, there's no need to do this migration
1. Migrate from Cloud Datastore to (native) Cloud Firestore
    - If your app (Cloud project) uses Datastore, you cannot use Firestore.
    - Requires new project as Cloud Datastore & Cloud Firestore mutually-exclusive
    - Most developers will NOT do this migration unless you *must have* Firestore's Firebase features
1. Migrate from App Engine to Cloud Run (using Cloud Datastore)
    - Migrate your app to a container with Docker
    - Alternative container migration with Buildpacks (see Step "5a" below)

## Summary

The table below summarizes each migration step and which options are available for developers after each step. Each step has a corresponding directory representing the state of the sample app after the previous migration step. The first step ("step0") represents the initial Python 2.7 App Engine app built using `ndb` and `webapp2`.

Python 2 | Next | Python 3 | Description
--- | --- | --- | ---
`step0-webapp2-gaendb-py2` | &dArr; | _N/A_ | Original GAE sample on GAE `ndb` & `webapp2`
`step1-flask-gaendb-py2` | &dArr; | _N/A_ | Migrate to Flask ("gaendb" _N/A_ for Python 3)
`step2-flask-cloudndb-py2` | &dArr; or &rArr; or &DownArrowBar;* | `step2-flask-cloudndb-py3` | Migrate to Cloud NDB
`step3-flask-datastore-py2` | &dArr; or &rArr; or &DownArrowBar;+ | `step3-flask-datastore-py3` | Migrate to Cloud Datastore
`step4-flask-firestore-py2` | &rArr; | `step4-flask-firestore-py3` | Migrate to Cloud Firestore
`step5-flask-cloudrun-py2` | &rArr; | `step5-flask-cloudrun-py3` | Migrate to Cloud Run (with Docker)

### Alternatives

We recommend users complete what we consider the minimum migration (Step 2) on Gen1. If there's no further interest in upgrading Datastore access nor migrating to Python 3, users can containerize their Python 2 apps for Cloud Run immediately (see Step 2a below). Who would you consider this? If you want to keep your app mostly as-is without additional migrations and want to containerize the app to make it more portable.

There are two ways to deploy containerized apps to Cloud Run, traditionally with Docker, or with the more recent [Cloud Buildpacks](https://github.com/GoogleCloudPlatform/buildpacks) (no Docker knowledge needed). Going from Step 3 to 5 uses Docker while going from Step 3 to 5a uses Cloud Buildpacks. (Step 5a is only available in Python 3.)

Python 2 | Next | Python 3 | Description
--- | --- | --- | ---
*`step2a-flask-cloudndb-py2-cloudrun` | _N/A_ | _N/A_ | Migrate (Python 2, Flask, Cloud NDB app) to Cloud Run (with Docker)
_N/A_ | _N/A_ | +`step5a-flask-datastore-py3-cloudrun` | Migrate to Cloud Run (with Cloud Buildpacks)

### Canonical code samples

Links to a more complete, canonical sample app will be provided if available. Example: the [GAE NDB to Cloud NDB migration sample](https://github.com/GoogleCloudPlatform/python-docs-samples/tree/master/appengine/standard/migration/ndb/overview) featured in the App Engine [migration documentation](https://cloud.google.com/appengine/docs/standard/python/migrate-to-python3).

## References

- App Engine Migration
    - [Migrate from Python 2 to 3 (Gen1 to Gen2)](http://cloud.google.com/appengine/docs/standard/python/migrate-to-python3) (Steps 2-5)
    - [Migrate from App Engine NDB to Cloud NDB](http://cloud.google.com/appengine/docs/standard/python/migrate-to-python3/migrate-to-cloud-ndb) (Step 2)
    - [App Engine NDB to Cloud NDB official sample app](https://github.com/GoogleCloudPlatform/python-docs-samples/tree/master/appengine/standard/migration/ndb/overview) (Step 2)
    - [App Engine `app.yaml` to Cloud Run `service.yaml` tool](http://googlecloudplatform.github.io/app-engine-cloud-run-converter) (Step 5a)
    - [Migrate from App Engine `db` to `ndb`](http://cloud.google.com/appengine/docs/standard/python/ndb/db_to_ndb) (Step -1 [before Step 0])

- Python App Engine
    - [Python 2 App Engine (Standard; Gen1)](https://cloud.google.com/appengine/docs/standard/python/runtime)
    - [Python 3 App Engine (Standard; Gen2)](https://cloud.google.com/appengine/docs/standard/python3/runtime)
    - [Python App Engine (Flexible; Gen2)](https://cloud.google.com/appengine/docs/flexible/python)

- Google Cloud Platform (GCP)
    - [Python on the Google Cloud Platform](https://cloud.google.com/python)
    - [GCP product client libraries](https://cloud.google.com/apis/docs/cloud-client-libraries)
    - [GCP documentation](https://cloud.google.com/docs)
