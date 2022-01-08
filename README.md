# Modernizing Google Cloud serverless compute applications
### To the latest Cloud services and serverless platforms

This is the corresponding repository to the [Serverless Migration Station](https://bit.ly/3xk2Swi) video series whose goal is to help users on a Google Cloud serverless compute platform modernize to newer Cloud products or other serverless compute platforms. Each modernization migration aims to feature a video, codelab (self-paced, hands-on tutorial), and code samples. The content initially focuses on App Engine and Google's earliest Cloud users.

[Google App Engine](https://cloud.google.com/appengine) (Standard) has undergone significant changes between the legacy and next generation platforms. To address this, we've created a set of codelabs (free, online, self-paced, hands-on tutorials) and corresponding videos (when available) to show developers how to perform individual migrations they can apply to modernize their apps for the latest runtimes, with this repo managing the samples from those codelabs. Codelab content typically falls into one of these three topics:

1. Migrate from a legacy App Engine service to a Cloud equivalent product
1. Migrate to a newer Cloud product, service, or API client library
1. Migrate to another or newer Google Cloud serverless compute platform

Each codelab begins with a "START" code base then walks developers through that migration step, resulting in a "FINISH" repo. If you make any mistakes along the way, you can always go back to START or compare your code with what's in the FINISH folder to see the differences. We also want to help you port to the Python 3 runtime, so some codelabs contain a bonus section for that purpose.

> **NOTE:** These migrations are *typically* aimed at Python 2 users
> 1. *Python 3.x App Engine users*: You're *already* on the next-gen platform, so only look for **non**-legacy service migrations
> 1. *Python 2.5 App Engine users*: to revive apps from the original 2.5 runtime, [deprecated in 2013](http://googleappengine.blogspot.com/2013/03/python-25-thanks-for-good-times.html) and [shutdown in 2017](https://cloud.google.com/appengine/docs/standard/python/python25), you must [migrate from `db` to `ndb`](http://cloud.google.com/appengine/docs/standard/python/ndb/db_to_ndb) and get those apps running on Python 2.7 before attempting these migrations.


## Prerequisites

- A Google account (Google Workspace/G Suite accounts may require administrator approval)
- A Google Cloud (GCP) project with an active billing account
- Familiarity with operating system terminal/shell commands
- Familiarity with developing &amp; deploying Python 2 apps to App Engine
- General skills in Python 2 and 3


## Cost

App Engine, Cloud Functions, and Cloud Run are not free services. While you may not have needed to enable billing in App Engine's early days, [all applications now require an active billing account](https://cloud.google.com/appengine/docs/standard/payment-instrument) backed by a financial instrument (usually a credit card). Don't worry, App Engine (and other GCP products) still have an ["Always Free" tier](https://cloud.google.com/free/docs/gcp-free-tier#free-tier-usage-limits) and as long as you stay within those limits, you won't incur any charges. Also check the App Engine [pricing](https://cloud.google.com/appengine/pricing) and [quotas](https://cloud.google.com/appengine/quotas) pages for more information.

Furthermore, deploying to GCP serverless platforms incur [minor build and storage costs](https://cloud.google.com/appengine/pricing#pricing-for-related-google-cloud-products). [Cloud Build](https://cloud.google.com/build/pricing) has its own free quota as does [Cloud Storage](https://cloud.google.com/storage/pricing#cloud-storage-always-free). For greater transparency, Cloud Build builds your application image which is than sent to the [Cloud Container Registry](https://cloud.google.com/container-registry/pricing), or [Artifact Registry](https://cloud.google.com/artifact-registry/pricing), its successor; storage of that image uses up some of that (Cloud Storage) quota as does network egress when transferring that image to the service you're deploying to. However you may live in region that does not have such a free tier, so be aware of your storage usage to minimize potential costs. (You may look at what storage you're using and how much, including deleting build artifacts via [your Cloud Storage browser](https://console.cloud.google.com/storage/browser).)


## Why

In App Engine's early days, users wanted Google to make the platform more flexible for developers and make their apps more portable. As a result, the team made significant changes to its 2nd-generation service which [launched in 2018](https://cloud.google.com/blog/products/gcp/introducing-app-engine-second-generation-runtimes-and-python-3-7). As a result, there are no longer any built-in services, allowing users to select from standalone GCP products or best-of-breed 3rd-party tools used by the broader community. Summary:

- **Legacy platform**: *Python 2* only, legacy built-in services
- **Next generation**: *Python 3* only, use standalone services, flexible platform, some* built-in services available

<sup>*</sup> see [Legacy services](#accessing-legacy-services-in-second-generation) section below

While the 2nd-gen platform is more flexible, users of the legacy platform have two challenges:

1. Migrate to unbundled/standalone services
1. Porting to a modern language release

Neither upgrade may be particularly straightforward and can only be done serially. On top of this, direct replacements are not available for all formerly built-in services; alternatives come in 3 flavors:

1. **Direct replacement**: Legacy services which matured into their own Cloud products *(e.g., App Engine Datastore is now [Cloud Datastore](http://cloud.google.com/datastore))*
1. **Partial replacement**: Some aspects of legacy services *(e.g., [Cloud Tasks](http://cloud.google.com/tasks) supports App Engine **push** tasks; for pull tasks, [Cloud Pub/Sub](http://cloud.google.com/pubsub) is recommended; use of [Cloud MemoryStore with REDIS](http://cloud.google.com/memorystore/docs/redis) as an alternative for Memcache)*
1. **No replacement**: No direct replacement available, so third-party or other tools recommended *(e.g., Search, Images, Users, Email)*

These are the challenges developers are facing, so the purpose of this content is to reduce the friction in this process and make things more prescriptive. Review the [runtimes chart](https://cloud.google.com/appengine/docs/standard/runtimes) to see the legacy services and current migration recommendation. The [migration guide overview](https://cloud.google.com/appengine/docs/standard/python/migrate-to-python3/migrating-services) has more information.

> **NOTE:** App Engine ([Flexible](https://cloud.google.com/appengine/docs/flexible/python/runtime?hl=en#interpreter)) is a next-gen service but is not within the scope of these tutorials. Curious developers can compare App Engine [Standard vs. Flexible](https://cloud.google.com/appengine/docs/the-appengine-environments) to find out more. Also, many of the Flexible use cases can now be handled by [Cloud Run](http://cloud.run).


## Progression (START and FINISH)

All codelabs begin with code in a START repo folder and end with code in a FINISH folder, implementing a single migration. Upon completion, users should confirm their code (for the most part) matches what's in the FINISH folder. The baseline migration sample app (Module 0; link below) is a barebones Python 2.7 App Engine app that uses the `webapp2` web framework plus the `ndb` Datastore library.

1. With _Module 0_ as the STARTing point, the Module 1 codelab migrates from the `webapp2` web framework to Flask, FINISHing at code matching the _Module 1_ repo.
1. Next, STARTing with the _Module 1_ application code (yours or ours), _Module 2_ migrates from  `ndb` to Cloud NDB, ending with code matching the (Module 2) FINISH repo folder. There's also has a bonus migration to Python 3, resulting in another FINISH repo folder, this one deployed on the next-generation platform.
1. _Your_ Python 2 apps may be using other built-in services like Task Queues or Memcache, so additional migration modules follow, some more optional than others, and not all are available yet (keep checking back here for updates).

Beyond Module 2, with some exceptions, **there is no specific order** of what migrations modules to tackle next. It depends on your needs (and your applications').


## Migration modules

The table below summarizes migration module resources currently available along with a more detailed table of contents below. Be sure to check back for updates as more resources are planned.


### Summary table

Module | Topic | Video | Codelab | START here | FINISH here
--- | --- | --- | --- | --- | ---
0|Baseline app| [link](http://twitter.com/googledevs/status/1407755281786867714?utm_source=twitter&utm_medium=unpaidsoc&utm_campaign=CDR_wes_aap-serverless_smsintro_201023&utm_content=-) | _N/A_ (no tutorial; just review the code) | _N/A_ | Module 0 [code](/mod0-baseline) (2.x)
1|Migrate to Flask| [link](https://twitter.com/googledevs/status/1413273119071031299?utm_source=twitter&utm_medium=unpaidsoc&utm_campaign=CDR_wes_aap-serverless_mgrwa2flsk_201008&u%20tm_content=-) | [link](http://g.co/codelabs/pae-migrate-flask) | Module 0 [code](/mod0-baseline) (2.x) | Module 1 [code](/mod1-flask) (2.x) &amp; [code](/mod1b-flask) (3.x)
2|Migrate to Cloud NDB| [link](https://twitter.com/googledevs/status/1417892493383802883?utm_source=twitter&utm_medium=unpaidsoc&utm_campaign=CDR_wes_aap-serverless_mgrcloudndb_201021&utm_content=-) | [link](http://g.co/codelabs/pae-migrate-cloudndb) | Module 1 [code](/mod1-flask) (2.x) | Module 2 [code](/mod2a-cloudndb) (2.x) &amp; [code](/mod2b-cloudndb) (3.x)
3|Migrate to Cloud Datastore| [link](http://twitter.com/googledevs/status/1422966928910393347?utm_source=twitter&utm_medium=unpaidsoc&utm_campaign=CDR_wes_aap-serverless_mgrcloudds_201003&utm_content=-) | [link](http://g.co/codelabs/pae-migrate-datastore) | Module 2 [code](/mod2a-cloudndb) (2.x) &amp; [code](/mod2b-cloudndb) (3.x) | Module 3 [code](/mod3a-datastore) (2.x) &amp; [code](/mod3b-datastore) (3.x)
4|Migrate to Cloud Run with Docker| [link](https://twitter.com/googledevs/status/1428041270702735362?utm_source=twitter&utm_medium=unpaidsoc&utm_campaign=CDR_wes_aap-serverless_mgrcrdckr_sms_201017&utm_content=-)| [link](http://g.co/codelabs/pae-migrate-rundocker) | Module 2 [code](/mod2a-cloudndb) (2.x) &amp; Module 3 [code](/mod3b-datastore) (3.x) | Module 4 [code](/mod4a-rundocker) (2.x) &amp; [code](/mod4b-rundocker) (3.x)
5|Migrate to Cloud Run with Buildpacks| [link](https://twitter.com/googledevs/status/1433113274984271875?utm_source=twitter&utm_medium=unpaidsoc&utm_campaign=CDR_wes_aap-serverless_mgrcrbdpk_sms_201031&utm_content=-) | [link](http://g.co/codelabs/pae-migrate-runbldpks) | Module 2 [code](/mod2b-cloudndb) (3.x) | Module 5 [code](/mod5-runbldpks) (3.x)
6|Migrate to Cloud Firestore| _N/A_ | _N/A_ | Module 3 [code](/mod3b-datastore) (3.x) | _no work required; [Datastore upgrade automatic](https://cloud.google.com/datastore/docs/upgrade-to-firestore)_
7|Add App Engine `taskqueue` push tasks| [link](https://twitter.com/googledevs/status/1443410302113099778?utm_source=twitter&utm_medium=unpaidsoc&utm_campaign=CDR_wes_aap-serverless_mgrgaetasks_sms_201028&utm_content=-) | [link](http://g.co/codelabs/pae-migrate-gaetasks) | Module 1 [code](/mod1-flask) (2.x) | Module 7 [code](/mod7-gaetasks) (2.x) &amp; [code](/mod7b-gaetasks) (3.x)
8|Migrate to Cloud Tasks| [link](https://twitter.com/googledevs/status/1450960021018267656?utm_source=twitter&utm_medium=unpaidsoc&utm_campaign=CDR_wes_aap-serverless_mgrcloudtasks_sms_201112&utm_content=-) | [link](http://g.co/codelabs/pae-migrate-cloudtasks) | Module 7 [code](/mod7-gaetasks) (2.x) | Module 8 [code](/mod8-cloudtasks) (2.x)
9|Migrate to Python 3, Cloud Datastore &amp; Cloud Tasks v2| _TBD_ | _TBD_ | Module 8 [code](/mod8-cloudtasks) (2.x) | _TBD_
10|Migrate Datastore/Firestore data to another project| _TBD_ | _N/A_ | _N/A_ | _TBD_
11|Migrate to Cloud Functions| _TBD_ | [link](https://codelabs.developers.google.com/codelabs/cloud-gae-python-migrate-11-functions?utm_source=codelabs&utm_medium=et&utm_campaign=CDR_wes_aap-serverless_mgrcloudfuncs_sms_202006&utm_content=-) | Module 2 [code](/mod2b-cloudndb) (3.x) | Module 11 [code](/mod11-functions) (3.x)
12|Add App Engine `memcache`| _TBD_ | [link](https://codelabs.developers.google.com/codelabs/cloud-gae-python-migrate-12-memcache?utm_source=codelabs&utm_medium=et&utm_campaign=CDR_wes_aap-serverless_mgrcloudfuncs_sms_202006&utm_content=-) | Module 1 [code](/mod1-flask) (2.x) | Module 12 [code](/mod12-memcache) (2.x) &amp; [code](/mod12b-memcache) (3.x)
13|Migrate to Cloud Memorystore| _TBD_ | _TBD_ | Module 12 [code](/mod12-memcache) (2.x) &amp; [code](/mod12b-memcache) (3.x) | Module 13 [code](/mod13a-memorystore) (2.x) &amp; [code](/mod13b-memorystore) (3.x)


### Table of contents

If there is a logical codelab to do immediately after completing one, they will be designated as NEXT. Other recommended codelabs will be listed as RECOMMENDED, and the more optional ones will be labeled as OTHERS (and usually in some kind of priority order).


- [Module 1 codelab](https://codelabs.developers.google.com/codelabs/cloud-gae-python-migrate-1-flask?utm_source=codelabs&utm_medium=et&utm_campaign=CDR_wes_aap-serverless_mgrwa2flsk_201008&utm_content=-): **Migrate from `webapp2` to [Flask](https://flask.palletsprojects.com)**
    - **Required** migration (can also pick your own framework)
        - `webapp2` does not do routing thus unsupported by App Engine (even though a [3.x port exists](https://github.com/fili/webapp2-gae-python37))
    - Python 2 only
        - START:  [Module 0 code - Baseline](/mod0-baseline) (2.x)
        - FINISH: [Module 1 code - Framework](/mod1-flask) (2.x)
    - NEXT:
        - Module 2 - migrate to Cloud NDB

- [Module 2 codelab](https://codelabs.developers.google.com/codelabs/cloud-gae-python-migrate-2-cloudndb?utm_source=codelabs&utm_medium=et&utm_campaign=CDR_wes_aap-serverless_mgrcloudndb_201021&utm_content=-): **Migrate from App Engine `ndb` to [Cloud NDB](https://googleapis.dev/python/python-ndb/latest)**
    - **Required** migration
        - Migration to Cloud NDB which is supported by Python 3 and the next-gen platform.
    - Python 2
        - START:  [Module 1 code - Framework](/mod1-flask) (2.x)
        - FINISH: [Module 2 code - Cloud NDB](/mod2a-cloudndb) (2.x)
    - Codelab bonus port to Python 3.x
        - FINISH: [Module 2 code - Cloud NDB](/mod2b-cloudndb) (3.x)
    - RECOMMENDED:
        - Module 7 - add App Engine (push) tasks
    - OTHERS (somewhat priority order):
        - Module 11 - migrate to Cloud Functions
        - Module 5 - migrate to Cloud Run container with Cloud Buildpacks
        - Module 4 - migrate to Cloud Run container with Docker
        - Module 3 - migrate to Cloud Datastore

- [Module 7 codelab](https://codelabs.developers.google.com/codelabs/cloud-gae-python-migrate-7-gaetasks?utm_source=codelabs&utm_medium=et&utm_campaign=CDR_wes_aap-serverless_mgrgaetasks_sms_201028&utm_content=-): **Add App Engine (push) Task Queues to App Engine `ndb` Flask app**
    - **Not a migration**: add GAE Task Queues to prepare for migration to Cloud Tasks
    - Python 2
        - START:  [Module 1 code - Framework](/mod1-flask) (2.x)
        - FINISH: [Module 7 code - GAE Task Queues](/mod7-gaetasks) (2.x)
    - NEXT: Module 8 - migrate App Engine push tasks to Cloud Tasks

- [Module 8 codelab](https://codelabs.developers.google.com/codelabs/cloud-gae-python-migrate-8-cloudtasks?utm_source=codelabs&utm_medium=et&utm_campaign=CDR_wes_aap-serverless_mgrcloudtasks_sms_201112&utm_content=-): **Migrate from App Engine (push) Task Queues to [Cloud Tasks](http://cloud.google.com/tasks) v1**
    - **Required** migration
        - Migration to Cloud Tasks which is supported by Python 3 and the next-gen platform.
        - Note this is only push tasks... pull tasks will be handled in a different codelab.
    - Python 2
        - START:  [Module 7 code - GAE Task Queues](/mod7-gaetasks) (2.x)
        - FINISH: [Module 8 code - Cloud Tasks](/mod8-cloudtasks) (2.x)
    - NEXT: Module 9 - migrate to Python 3 and Cloud Datastore

- **Module 9 codelab** (TBD): **Migrate a Python 2 Cloud NDB &amp; Cloud Tasks (v1) app to a Python 3 Cloud Datastore &amp; Cloud Tasks (v2) app**
    - **Optional** migrations
        - Migrating to Python 3 is not required but recommended as Python 2 has been sunset
        - Migrating to Cloud Firestore is *very* optional as Cloud NDB works on 3.x and most importantly, Cloud Firestore requires a completely new GCP project
    - Python 2
        - START:  [Module 8 code - Cloud Tasks](/mod8-cloudtasks) (2.x)
    - Python 3
        - FINISH: _TBD_
    - RECOMMENDED:
        - Module 11 - migrate to Cloud Functions
        - Module 5 - migrate to Cloud Run container with Cloud Buildpacks
        - Module 4 - migrate to Cloud Run container with Docker

- [Module 4 codelab](https://codelabs.developers.google.com/codelabs/cloud-gae-python-migrate-4-rundocker?utm_source=codelabs&utm_medium=et&utm_campaign=CDR_wes_aap-serverless_mgrcrdckr_sms_201017&utm_content=-): **Migrate from App Engine to Cloud Run with Docker**
    - **Optional** migration
        - "Containerize" your app (migrate your app to a container) with Docker
    - Python 2
        - START:  [Module 2 code - Cloud NDB](/mod2a-cloudndb) (2.x)
        - FINISH: [Module 4 code - Cloud Run - Docker 3.x](/mod4a-rundocker) (2.x)
    - Python 3
        - START:  [Module 3 code - Cloud Datastore](/mod3b-datastore) (3.x)
        - FINISH: [Module 4 code - Cloud Run - Docker](/mod4b-rundocker) (3.x)
    - RECOMMENDED:
        - Module 5 - migrate to Cloud Run container with Cloud Buildpacks
    - OTHER OPTIONS (in somewhat priority order):
        - Module 7 - add App Engine (push) tasks
        - Module 11 - migrate to Cloud Functions

- [Module 5 codelab](https://codelabs.developers.google.com/codelabs/cloud-gae-python-migrate-5-runbldpks?utm_source=codelabs&utm_medium=et&utm_campaign=CDR_wes_aap-serverless_mgrcrbdpk_sms_201031&utm_content=-): **Migrate from App Engine to Cloud Run with Cloud Buildpacks**
    - **Optional** migration
        - "Containerize" your app (migrate your app to a container) with...
        - [Cloud Buildpacks]() which lets you containerize your app without `Dockerfile`s
    - Python 3 only
        - START:  [Module 2 code - Cloud NDB](/mod2b-cloudndb) (3.x)
        - FINISH: [Module 5 code - Cloud Run - Buildpacks 3.x](/mod5-runbldpks) (3.x)
    - RECOMMENDED:
        - Module 4 - migrate to Cloud Run container with Docker
    - OTHER OPTIONS (in somewhat priority order):
        - Module 7 - add App Engine (push) tasks
        - Module 11 - migrate to Cloud Functions

- [Module 3 codelab](https://codelabs.developers.google.com/codelabs/cloud-gae-python-migrate-3-datastore?utm_source=codelabs&utm_medium=et&utm_campaign=CDR_wes_aap-serverless_mgrcloudds_201003&utm_content=-): **Migrate from Cloud NDB to [Cloud Datastore](http://cloud.google.com/datastore)**
    - **Optional** migration
        - Recommended only if using Cloud Datastore elsewhere (GAE *or* non-App Engine) apps
        - Helps w/code consistency &amp; reusability, reduces maintenance costs
    - Python 2
        - START:  [Module 2 code - Cloud NDB](/mod2a-cloudndb) (2.x)
        - FINISH: [Module 3 code - Cloud Datastore](/mod3a-datastore) (2.x)
    - Python 3
        - START:  [Module 2 code - Cloud NDB](/mod2b-cloudndb) (3.x)
        - FINISH: [Module 3 code - Cloud Datastore](/mod3b-datastore) (3.x)
    - RECOMMENDED:
        - Module 7 - add App Engine (push) tasks
    - OTHER OPTIONS (in somewhat priority order):
        - Module 11 - migrate to Cloud Functions
        - Module 5 - migrate to Cloud Run container with Cloud Buildpacks
        - Module 4 - migrate to Cloud Run container with Docker

- [Module 11 codelab](https://codelabs.developers.google.com/codelabs/cloud-gae-python-migrate-11-functions?utm_source=codelabs&utm_medium=et&utm_campaign=CDR_wes_aap-serverless_mgrcloudfuncs_sms_202006&utm_content=-): **Migrate from App Engine to Cloud Functions**
    - **Optional** migration
        - Recommende for small apps or for breaking up large apps into multiple microservices
    - Python 3 only
        - START:  [Module 2 code - Cloud NDB](/mod2b-cloudndb) (3.x)
        - FINISH: [Module 11 code - Cloud Firestore](/mod11-functions) (3.x)
    - RECOMMENDED:
        - Module 7 - add App Engine (push) tasks
    - OTHER OPTIONS (in somewhat priority order):
        - Module 5 - migrate to Cloud Run container with Cloud Buildpacks
        - Module 4 - migrate to Cloud Run container with Docker
        - Module 3 - migrate to Cloud Datastore


## Considerations for mobile developers

If your original app users does *not* have a user interface, i.e., mobile backends, etc., but still uses `webapp2` for routing, some migration must still be completed. Your options:
- Migrate to Flask (or another) web framework but keep app on App Engine
- Use [Cloud Endpoints](http://cloud.google.com/endpoints) or [Cloud API Gateway](https://cloud.google.com/api-gateway) for your mobile endpoints
- Break-up your monolithic app to "microservices" and migrate your app to either:
    - [Google Cloud Functions](https://cloud.google.com/functions)
    - [Firebase mobile &amp; web app platform](https://firebase.google.com) (and [Cloud Functions for Firebase](https://firebase.google.com/products/functions) [customized for Firebase])


## Canonical code samples

- This repo, along with corresponding codelabs &amp; videos are complementary to the official docs &amp; code samples.
    - The [official Python 2 to 3 migration documentation](https://cloud.google.com/appengine/docs/standard/python/migrate-to-python3)
    - [Canonical migration code samples repo](https://github.com/GoogleCloudPlatform/python-docs-samples/tree/master/appengine/standard/migration)
        - *Example:* [GAE `ndb` to Cloud NDB](https://github.com/GoogleCloudPlatform/python-docs-samples/tree/master/appengine/standard/migration/ndb/overview) (similar to Module 2)
        - *Example:* [GAE `taskqueue` to Cloud Tasks](https://github.com/GoogleCloudPlatform/python-docs-samples/tree/master/appengine/standard/migration/taskqueue) (similar to Module 8)


## Accessing legacy services in second generation

Many legacy App Engine first generation platform (Python 2, Java 8, PHP 5, and Go 1.11 &amp; older) services are available ([as of Sep 2021](https://twitter.com/googledevs/status/1445916786755571712) for second generation runtimes (Python 3, Java 11, PHP 7, and Go 1.12 &amp; newer) in a public preview. There are no videos or codelabs yet, however the Module 1 Flask migration using App Engine `ndb` [Python 2 sample ](/mod1-flask) is available in [Python 3](/mod1b-flask) if you have access. Similarly, Python 3 editions are also available for Modules 7 and 12 which add usage of App Engine `taskqueue` and `memcache`, respectively.


## References

- App Engine Migration
    - [Migrate from Python 2 to 3](http://cloud.google.com/appengine/docs/standard/python/migrate-to-python3)
    - [Migrate from App Engine `ndb` to Cloud NDB](http://cloud.google.com/appengine/docs/standard/python/migrate-to-python3/migrate-to-cloud-ndb) (Module 2)
    - [Migrate from App Engine `taskqueue` to Cloud Tasks](http://cloud.google.com/appengine/docs/standard/python/migrate-to-python3/migrate-to-cloud-ndb) (Modules 7-9)
    - [Migrate from App Engine `db` to `ndb`](http://cloud.google.com/appengine/docs/standard/python/ndb/db_to_ndb) ("Module -1"; only for reviving "dead" Python 2.5 apps for 2.7)
    - [Community contributed migration samples](https://github.com/GoogleCloudPlatform/appengine-python2-3-migration)

- Python App Engine
    - [App Engine 1st vs. 2nd generation runtimes](https://cloud.google.com/appengine/docs/standard/runtimes)
    - [Python 2 App Engine (Standard) runtime](https://cloud.google.com/appengine/docs/standard/python/runtime)
    - [Python 3 App Engine (Standard) runtime](https://cloud.google.com/appengine/docs/standard/python3/runtime)
    - [Python App Engine (Flexible)](https://cloud.google.com/appengine/docs/flexible/python)

- Google Cloud Platform (GCP)
    - [Python on GCP](https://cloud.google.com/python)
    - [Cloud client libraries](https://cloud.google.com/apis/docs/cloud-client-libraries)
    - [All GCP documentation](https://cloud.google.com/docs)
