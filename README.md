# Python 2 App Engine app migration
### To modern runtime, Cloud services, Python 3, and Cloud Run containers

[Google App Engine](https://cloud.google.com/appengine) (Standard) has undergone significant changes between the legacy and next generation platforms. To address this, we've created a set of codelab tutorials (and this code repo) to show developers how to perform individual migrations they can apply to modernize their apps for the latest runtimes.

Codelabs begin with a "START" code base then walks developers through that migration step, resulting in a "FINISH" repo. If you made any mistakes along the way, you can always go back to START or compare your code with that in the FINISH folder to see the differences. Since another goal is to port to Python 3, some codelabs have a bonus section for that purpose.

> **NOTE:** These migrations are *only* for those with Python 2 (2.7) App Engine apps.
> 1. *Python 3.x App Engine users*: You're *already* on the next-gen platform, so there's no need for you to be here unless you help 2.x developers migrate.
> 1. *Python 2.5 App Engine developers*: to revive apps on the original 2.5 runtime, [deprecated in 2013](http://googleappengine.blogspot.com/2013/03/python-25-thanks-for-good-times.html) and [shutdown in 2017](https://cloud.google.com/appengine/docs/standard/python/python25), you must [migrate from `db` to `ndb`](http://cloud.google.com/appengine/docs/standard/python/ndb/db_to_ndb) before attempting these migrations.


## Prerequisites

- A Google account (G Suite accounts may require administrator approval)
- A Google Cloud (GCP) project with an active billing account
- Familiarity with operating system terminal/shell commands
- Familiarity with developing &amp; deploying Python 2 apps to App Engine
- General skills in Python 2 and 3


## Cost

App Engine is not a free service. While you may not have needed to enable billing in App Engine's early days, [all applications now require an active billing account](https://cloud.google.com/appengine/docs/standard/payment-instrument) backed by a financial instrument (usually a credit card). Don't worry, App Engine (and other GCP products) still have an ["Always Free" tier](https://cloud.google.com/free/docs/gcp-free-tier#always-free), and as long as you stay within those limits, you won't incur billing. Also check the App Engine [pricing](https://cloud.google.com/appengine/pricing) and [quotas](https://cloud.google.com/appengine/quotas) pages for more information.


## Why

In App Engine's early days, users wanted Google to make the platform more flexible for developers and make their apps more portable. As a result, the team made significant changes to its 2nd-generation service which launched in 2017. As a result, all previously built-in services have been removed, and users can either choose from new standalone Cloud products as replacements or best-of-breed replacements in the broader developer community. Summary:

- **Legacy platform**: *Python 2* only, proprietary built-in services
- **Next generation**: *Python 3* only, *no* proprietary built-in services

The key issue is that developers looking to port their applications to Python 3 have two **huge** hurdles to overcome, migrating from Python 2 to 3 **and** migrating from built-in services to alternatives. On top of this, direct replacements are not available for all built-in services; alternatives come in 3 flavors:

1. **Direct replacement**: Legacy services which matured into their own Cloud products *(e.g., App Engine Datastore is now [Cloud Datastore](http://cloud.google.com/datastore))*
1. **Partial replacement**: Some aspects of legacy services *(e.g., [Cloud Tasks](http://cloud.google.com/tasks) supports App Engine **push** tasks; for pull tasks, [Cloud Pub/Sub](http://cloud.google.com/pubsub) is recommended; use of [Cloud MemoryStore with REDIS](http://cloud.google.com/memorystore/docs/redis) as an alternative for Memcache)*
1. **No replacement**: No direct replacement available, so third-party or other tools recommended *(e.g., Search, Images, Users, Email)*

These are the challenges developers are facing, so the purpose of this content is to make this process more smooth and prescriptive. Review the [runtimes chart](https://cloud.google.com/appengine/docs/standard/runtimes) to see the legacy services and current migration recommendation. The [migration guide overview](https://cloud.google.com/appengine/docs/standard/python/migrate-to-python3/migrating-services) has more information.

> **NOTE:** App Engine ([Flexible](https://cloud.google.com/appengine/docs/flexible/python/runtime?hl=en#interpreter)) is a next-gen service but is not within the scope of these tutorials. Developers who are curious can compare App Engine [Standard vs. Flexible](https://cloud.google.com/appengine/docs/the-appengine-environments).


## Progression

All codelabs begin with code in a START repo and ends with a FINISH repo folder, completing a single migration. Users who complete the tutorial should confirm their code (for the most part) matches what's in the FINISH folder. The Module 0 repo contains a barebones Python 2.7 App Engine app that uses the `webapp2` web framework plus the `ndb` Datastore library. It represents the baseline migration sample app.

1. From there, Module 1 migrates away from `webapp2` to Flask, migrating the Module 0 code (START) to end with the Module 1 folder.

1. The Module 2 codelab migrates away from  `ndb` to Cloud NDB, STARTs with the Module 1 repo (ours or yours), and ends with the Module 2 (Python 2) FINISH repo folder. Module 2's codelab also has a bonus migration to Python 3, resulting in code that should match the Module 2 (Python 3) repo. Once you've arrived at Module 2's Python 3 code, your app is modernized and runs on the next-generation platform.

Of course, things aren't as simple in real life. Your Python 2 App Engine app may also be using Task Queues, Memcache, or many of the other original App Engine built-in services, so those will be additional migration modules (not all are available yet). With some exceptions, there's no specific order of what migrations you do next. It's just what you (or your apps) need. Here's full summary of what's currently available:


## Migrations

The table below summarizes migration module resources currently available to developers along with a more detailed table of contents below. Be sure to check back for updates as more resources are planned.

### Summary table

Module | Topic | Video | Codelab | START repo | FINISH repo
--- | --- | --- | --- | --- | ---
0|Baseline app| _TBD_ | _N/A_ | _N/A_ | Module 0 [code](/mod0-baseline) (2.x)
1|Migrate to Flask| _TBD_ | _TBD_ | Module 0 [code](/mod0-baseline) (2.x) | Module 1 [code](/mod1-framework) (2.x)
2|Migrate to Cloud NDB| _TBD_ | _TBD_ | Module 1 [code](/mod1-framework) (2.x) | Module 2 [code](/mod2a-cloudndb) (2.x) &amp; [code](/mod2b-cloudndb) (3.x)
3|Migrate to Cloud Datastore| _TBD_ | _TBD_ | Module 2 [code](/mod2a-cloudndb) (2.x) &amp; [code](/mod2b-cloudndb) (3.x) | Module 3 [code](/mod3a-datastore) (2.x) &amp; [code](/mod3b-datastore) (3.x)
4|Migrate to Cloud Run with Docker| _TBD_ | _TBD_ | Module 2 [code](/mod2a-cloudndb) (2.x) &amp; Module 3 [code](/mod3b-datastore) (3.x) | Module 4 [code](/mod4a-rundocker) (2.x) &amp; [code](/mod4b-rundocker) (3.x)
5|Migrate to Cloud Run with Buildpacks| _TBD_ | _TBD_ | Module 2 [code](/mod2b-cloudndb) (3.x) | Module 5 [code](/mod5-runbldpks) (3.x)
6|Migrate to Cloud Firestore| _TBD_ | _TBD_ | Module 3 [code]() (3.x) | Module 6 [code](/mod6-firestore) (3.x)
7|Add App Engine push tasks| _TBD_ | _TBD_ | Module 1 [code]() (2.x) | Module 7 [code](/mod7-gaetasks) (2.x)
8|Migrate to Cloud Tasks| _TBD_ | _TBD_ | Module 7 [code](/mod7-gaetasks) (2.x) | Module 8 [code](/mod8-cloudtasks) (2.x)
9|Migrate to Python 3 (Cloud Datastore &amp; Cloud Tasks v2)| _TBD_ | _TBD_ | Module 8 [code](/mod8-cloudtasks) (2.x) | Module 9 [code](/mod9-py3xlouddstasks) (3.x)

### Table of contents

If there is a logical codelab to do immediately after completing one, they will be designated as NEXT. Other recommended codelabs will be listed as RECOMMENDED, and the more optional ones will be labeled as OTHERS (and usually in some kind of priority order).

- Module 1 codelab: **Migrate from `webapp2` to [Flask](https://flask.palletsprojects.com)**
    - **Required** migration (can also pick your own framework)
        - `webapp2` does not do routing thus unsupported by App Engine (even though a [3.x port exists](https://github.com/fili/webapp2-gae-python37))
    - Python 2 only
        - START:  [Module 0 code - Baseline](/mod0-baseline) (2.x)
        - FINISH: [Module 1 code - Framework](/mod1-framework) (2.x)
    - NEXT: Module 2 codelab - migrate to Cloud NDB

- Module 2 codelab: **Migrate from App Engine `ndb` to [Cloud NDB](https://googleapis.dev/python/python-ndb/latest)**
    - **Required** migration
        - Migration to Cloud NDB which is supported by Python 3 and the next-gen platform.
    - Python 2
        - START:  [Module 1 code - Framework](/mod1-framework) (2.x)
        - FINISH: [Module 2 code - Cloud NDB](/mod2a-cloudndb) (2.x)
    - Codelab bonus port to Python 3.x
        - FINISH: [Module 2 code - Cloud NDB](/mod2b-cloudndb) (3.x)
    - RECOMMENDED:
        - Module 7 codelab - add App Engine (push) tasks
    - OTHERS (somewhat priority order):
        - Module 4 codelab - migrate to Cloud Run container with Docker
        - Module 5 codelab - migrate to Cloud Run container with Cloud Buildpacks
        - Module 3 codelab - migrate to Cloud Datastore

- Module 7 codelab: **Add App Engine (push) Task Queues to App Engine `ndb` Flask app**
    - **Not a migration**: add GAE Task Queues to prepare for migration to Cloud Tasks
    - Python 2
        - START:  [Module 1 code - Framework](/mod1-framework) (2.x)
        - FINISH: [Module 7 code - GAE Task Queues](/mod7-gaetasks) (2.x)
    - NEXT: Module 8 codelab - migrate App Engine push tasks to Cloud Tasks

- Module 8 codelab: **Migrate from App Engine (push) Task Queues to [Cloud Tasks](http://cloud.google.com/tasks) v1**
    - **Required** migration
        - Migration to Cloud Tasks which is supported by Python 3 and the next-gen platform.
        - Note this is only push tasks... pull tasks will be handled in a different codelab.
    - Python 2
        - START:  [Module 7 code - GAE Task Queues](/mod7-gaetasks) (2.x)
        - FINISH: [Module 8 code - Cloud Tasks](/mod8-cloudtasks) (2.x)
    - NEXT: Module 9 codelab - migrate to Python 3

- Module 9 codelab: **Migrate a Python 2 Cloud NDB &amp; Cloud Tasks app to a Python 3 Cloud Datastore app**
    - **Mixed migration recommendation**
        - Migrating to Python 3 is required, but...
        - Migrating to Cloud Datastore is optional as Cloud NDB works on 3.x; it's to give you the experience of doing it
        - This codelab includes the migration in the [Module 3 codelab](), so skip it
    - Python 2
        - START:  [Module 8 code - Cloud Tasks](/mod8-cloudtasks) (2.x)
    - Python 3
        - FINISH: [Module 9 code - Cloud Datastore &amp; Tasks](/mod9-py3clouddstasks) (3.x)
    - RECOMMENDED:
        - Module 4 codelab - migrate to Cloud Run container with Docker
        - Module 5 codelab - migrate to Cloud Run container with Cloud Buildpacks

- Module 4 codelab: **Migrate from App Engine to [Cloud Run](http://cloud.google.com/run) with Docker**
    - **Optional** migration
        - "Containerize" your app (migrate your app to a container) with Docker
    - Python 2
        - START:  [Module 2 code - Cloud NDB](/mod2a-cloudndb) (2.x)
        - FINISH: [Module 4 code - Cloud Run - Docker 3.x](/mod4a-rundocker) (2.x)
    - Python 3
        - START:  [Module 3 code - Cloud Datastore](/mod3b-datastore) (3.x)
        - FINISH: [Module 4 code - Cloud Run - Docker](/mod4b-rundocker) (3.x)
    - RECOMMENDED:
        - Module 5 codelab - migrate to Cloud Run container with Cloud Buildpacks

- Module 5 codelab: **Migrate from App Engine to [Cloud Run](http://cloud.google.com/run) with Cloud Buildpacks**
    - **Optional** migration
        - "Containerize" your app (migrate your app to a container) with...
        - [Cloud Buildpacks]() which lets you containerize your app without Dockerfiles
    - Python 3 only
        - START:  [Module 2 code - Cloud NDB](/mod2b-cloudndb) (3.x)
        - FINISH: [Module 5 code - Cloud Run - Buildpacks 3.x](/mod5-runbldpks) (3.x)

- Module 3 codelab: **Migrate from Cloud NDB to Cloud Datastore**
    - **Optional** migration
        - Recommended only if using Cloud Datastore elsewhere (GAE *or* non-App Engine) apps
        - Helps w/code consistency &amp; reusability, reduces maintenance costs
    - Python 2
        - START:  [Module 2 code - Cloud NDB](/mod2a-cloudndb) (2.x)
        - FINISH: [Module 3 code - Cloud Datastore](/mod3a-datastore) (2.x)
    - Python 3
        - START:  [Module 2 code - Cloud NDB](/mod2b-cloudndb) (3.x)
        - FINISH: [Module 3 code - Cloud Datastore](/mod3b-datastore) (3.x)
    - OPTIONS (in somewhat priority order):
        - Module 7 codelab - add App Engine (push) tasks
        - Module 4 codelab - migrate to Cloud Run container with Docker
        - Module 6 codelab - migrate to Cloud Firestore

- Module 6 codelab: **Migrate from Cloud Datastore to [Cloud Firestore](http://cloud.google.com/firestore)**
    - **Highly optional** migration (WARNING: infrequent/uncommon &amp; "expensive" migration)
        - Requires new project &amp; Datastore has better write performance (currently)
        - If you **must have** Firestore's Firebase features
    - Python 3 only
        - START:  [Module 3 code - Cloud Datastore](/mod3b-datastore) (3.x)
        - FINISH: [Module 6 code - Cloud Firestore](/mod6-firestore) (3.x)
    - RECOMMENDED:
        - Module 7 codelab - add App Engine (push) tasks
    - OTHER OPTIONS (in somewhat priority order):
        - Module 4 codelab - migrate to Cloud Run container with Docker


## Considerations for mobile developers

If your original app users does *not* have a user interface, i.e., mobile backends, etc., but still uses `webapp2` for routing, some migration must still be completed. Your options:
- Migrate to Flask (or another) web framework but keep app on App Engine
- Use [Cloud Endpoints](http://cloud.google.com/endpoints) or [Cloud API Gateway](https://cloud.google.com/api-gateway) for your mobile endpoints
- Break-up your monolithic app to "microservices" and migrate your app to either:
    - [Google Cloud Functions](https://cloud.google.com/functions)
    - [Firebase mobile &amp; web app platform](https://firebase.google.com) (and [Cloud Functions for Firebase](https://firebase.google.com/products/functions) [customized for Firebase])



### Canonical code samples

- This repo, along with corresponding codelabs &amp; videos are complementary to the official docs &amp; code samples.
    - The [official Python 2 to 3 migration documentation](https://cloud.google.com/appengine/docs/standard/python/migrate-to-python3)
    - [Canonical migration code samples repo](https://github.com/GoogleCloudPlatform/python-docs-samples/tree/master/appengine/standard/migration)
        - Example: [GAE `ndb` to Cloud NDB](https://github.com/GoogleCloudPlatform/python-docs-samples/tree/master/appengine/standard/migration/ndb/overview)
        - Example: [GAE `taskqueue` to Cloud Tasks](https://github.com/GoogleCloudPlatform/python-docs-samples/tree/master/appengine/standard/migration/taskqueue)


## References

- App Engine Migration
    - [Migrate from Python 2 to 3](http://cloud.google.com/appengine/docs/standard/python/migrate-to-python3)
    - [Migrate from App Engine `ndb` to Cloud NDB](http://cloud.google.com/appengine/docs/standard/python/migrate-to-python3/migrate-to-cloud-ndb) (Step 2)
    - [App Engine `ndb` to Cloud NDB official sample app](https://github.com/GoogleCloudPlatform/python-docs-samples/tree/master/appengine/standard/migration/ndb/overview) (Step 2)
    - [Migrate from App Engine `taskqueue` to Cloud Tasks](http://cloud.google.com/appengine/docs/standard/python/migrate-to-python3/migrate-to-cloud-ndb) (Steps 5a-5c)
    - [App Engine `app.yaml` to Cloud Run `service.yaml` tool](http://googlecloudplatform.github.io/app-engine-cloud-run-converter) (Step 4a)
    - [Migrate from App Engine `db` to `ndb`](http://cloud.google.com/appengine/docs/standard/python/ndb/db_to_ndb) ("Step -1"; only for reviving "dead" Python 2.5 apps for 2.7)

- Python App Engine
    - [Python 2 App Engine (Standard)](https://cloud.google.com/appengine/docs/standard/python/runtime)
    - [Python 3 App Engine (Standard)](https://cloud.google.com/appengine/docs/standard/python3/runtime)
    - [Python App Engine (Flexible)](https://cloud.google.com/appengine/docs/flexible/python)

- Google Cloud Platform (GCP)
    - [Python on GCP](https://cloud.google.com/python)
    - [Cloud client libraries](https://cloud.google.com/apis/docs/cloud-client-libraries)
    - [All GCP documentation](https://cloud.google.com/docs)
