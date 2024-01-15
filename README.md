| :boom: ALERT!!             |
|:---------------------------|
| This repo will soon be relocating to [GoogleCloudPlatform](https://github.com/GoogleCloudPlatform) as we better organize these code samples! Stay tuned as more info is coming soon. |


# Modernizing Google Cloud serverless compute applications
### To the latest Cloud services and serverless platforms

This is the corresponding repository to the [Serverless Migration Station](https://bit.ly/3xk2Swi) video series whose goal is to help users on a Google Cloud serverless compute platform modernize to other Cloud or serverless products. Modernization steps generally feature a video, codelab (self-paced, hands-on tutorial), and code samples. The content initially focuses on App Engine and Google's earliest Cloud users. Read more about the [codelabs in this announcement](https://developers.googleblog.com/2021/03/modernizing-your-google-app-engine-applications.html?utm_source=ext&utm_medium=partner&utm_campaign=CDR_wes_aap-serverless_modernizegae_codelabsannounce_201031&utm_content=-) as well as [this one introducing the video series](https://developers.googleblog.com/2021/06/introducing-serverless-migration.html?utm_source=blog&utm_medium=partner&utm_campaign=CDR_wes_aap-serverless_smsintro_201023). This repo is for Python developers; there is another repo for Java developers.

[Google App Engine](https://cloud.google.com/appengine) (Standard) has undergone significant changes between the legacy and next generation platforms. To address this, we've created a set of resources showing developers how to perform individual migrations that can be applied to modernize their apps for the latest runtimes, meaning to Python 3 even though [Google expressed long-term support for legacy runtimes](https://cloud.google.com/appengine/docs/standard/long-term-support) like Python 2. The content falls into one of these topics:

1. Migrate from a legacy App Engine service to a similar Cloud product
1. Shift to another Cloud serverless compute platform (e.g., from App Engine to Cloud Run)
1. General app, data, or service migration steps and best practices

Each codelab begins with a sample app in a "START" repo folder then walks developers through that migration, resulting in code in a "FINISH" repo. If you make mistakes along the way, you can always go back to START or compare your code with what's in the corresponding FINISH folder. The baseline apps are in Python 2, and since we also want to help you port to Python 3, some codelabs contain additional steps to do so.

> **NOTEs:**
> 1. These migrations are *typically* aimed at our earliest users, e.g., Python 2
> 1. *Python 3.x App Engine users*: You're *already* on the next-gen platform, so you would focus on migrating away from the legacy bundled services
> 1. *Python 2.5 App Engine users*: to revive apps from the original 2.5 runtime, [deprecated in 2013](http://googleappengine.blogspot.com/2013/03/python-25-thanks-for-good-times.html) and [shutdown in 2017](https://cloud.google.com/appengine/docs/standard/python/python25), you must [migrate from `db` to `ndb`](http://cloud.google.com/appengine/docs/standard/python/ndb/db_to_ndb) and get those apps running on Python 2.7 before attempting these migrations.


## Prerequisites

- A Google account and Cloud (GCP) project with an active billing account
- Familiarity with operating system terminal/shell commands
- Familiarity with developing &amp; deploying Python 2 apps to App Engine
- General skills in Python 2 and 3


## Cost

App Engine, Cloud Functions, and Cloud Run are not free services. While you may not have enabled billing in App Engine's early days, [all applications now require an active billing account](https://cloud.google.com/appengine/docs/standard/payment-instrument) backed by a financial instrument (usually a credit card). Don't worry, App Engine (and other GCP products) still have an ["Always Free" tier](https://cloud.google.com/free/docs/gcp-free-tier#free-tier-usage-limits) and as long as you stay within those limits, you won't incur any charges. Also check the App Engine [pricing](https://cloud.google.com/appengine/pricing) and [quotas](https://cloud.google.com/appengine/quotas) pages for more information.

Furthermore, deploying to GCP serverless platforms incur [minor build and storage costs](https://cloud.google.com/appengine/pricing#pricing-for-related-google-cloud-products). [Cloud Build](https://cloud.google.com/build/pricing) has its own free quota as does [Cloud Storage](https://cloud.google.com/storage/pricing#cloud-storage-always-free). For greater transparency, Cloud Build builds your application image which is than sent to the [Cloud Container Registry](https://cloud.google.com/container-registry/pricing), or [Artifact Registry](https://cloud.google.com/artifact-registry/pricing), its successor; storage of that image uses up some of that (Cloud Storage) quota as does network egress when transferring that image to the service you're deploying to. However you may live in region that does not have such a free tier, so be aware of your storage usage to minimize potential costs. (You may look at what storage you're using and how much, including deleting build artifacts via [your Cloud Storage browser](https://console.cloud.google.com/storage/browser).)


## Why

App Engine initially [launched in 2008](http://googleappengine.blogspot.com/2008/04/introducing-google-app-engine-our-new.html) ([video](http://youtu.be/3Ztr-HhWX1c)), providing a suite of bundled services making it convenient for developers to access a database (Datastore), caching (Memcache), independent task execution (Task Queue), large "blob" storage (Blobstore) to allow for end-user file uploads or to serve large media files, and other companion services. However, apps leveraging those services can only run their apps on App Engine.


To increase app portability, its 2nd-generation service [launched in 2018](https://cloud.google.com/blog/products/gcp/introducing-app-engine-second-generation-runtimes-and-python-3-7), initially removing those legacy bundled services. The main reason to move to the 2nd generation service is that it allows developers to upgrade to the latest language runtimes, such as moving from Python 2 to 3 or Java 8 to 17. Unfortunately, it was mutually exclusive to do so, meaning while you could upgrade language releases, you lost access to those bundled services, making it a showstopper for many users.

However, due to their popularity _and_ to help users upgrade, the App Engine team [restored access to many (but not all) of those services in Fall 2021](https://cloud.google.com/blog/products/serverless/support-for-app-engine-services-in-second-generation-runtimes). For more on this, see the [Legacy services](#accessing-legacy-services-in-second-generation) section below. As Google is continually striving to have the most [open cloud](https://cloud.google.com/open-cloud) on the market, and while many of those services are now available again, apps can _still_ be more portable if they migrated away from the legacy services to similar Cloud or 3rd-party offerings. Another issue with the bundled services is that they're only available in 2nd generation runtimes that have a 1st generation service (Python, Java, Go, PHP), excluding 2nd generation-only runtimes like Ruby and Node.js.

Once apps have moved away from App Engine bundled services to similar Cloud or 3rd-party services. apps are portable enough to:

1. Run on the [2nd generation App Engine service](https://cloud.google.com/appengine/docs/standard/runtimes)
1. Shift across to other serverless platforms, like [Cloud Functions](https://developers.googleblog.com/2022/04/how-can-app-engine-users-take-advantage-of-cloud-functions.html?utm_source=blog&utm_medium=partner&utm_campaign=CDR_wes_aap-serverless_mgrcloudfuncs_sms_202006) or Cloud Run ([with](https://developers.googleblog.com/2021/08/containerizing-google-app-engine-apps-for-cloud-run.html?utm_source=blog&utm_medium=partner&utm_campaign=CDR_wes_aap-serverless_mgrcrdckr_sms_201017) or [without](https://developers.googleblog.com/2021/09/an-easier-way-to-move-your-app-engine-to-cloud-run.html?utm_source=blog&utm_medium=partner&utm_campaign=CDR_wes_aap-serverless_mgrcrbdpk_sms_201031) Docker), or
1. Move to VM-based services like [GKE](https://cloud.google.com/gke) or [Compute Engine](https://cloud.google.com/compute), or to other compute platforms

> **NOTEs:**
> 1. App Engine ([Flexible](https://cloud.google.com/appengine/docs/flexible/python/runtime?hl=en#interpreter)) is a next-gen service but is not within the scope of these tutorials. Curious developers can compare App Engine [Standard vs. Flexible](https://cloud.google.com/appengine/docs/the-appengine-environments) to find out more.
> 1. Many use cases for Flexible or a desire for containerization can be handled by [Cloud Run](http://cloud.run).
> 1. Small apps or large monolithic apps broken up into multiple, independent microservices can consider migrating to [Cloud Functions](https://cloud.google.com/functions).


## Progression (what order to do things)

### "START" and "FINISH" repo folders

All codelabs begin with code in a START repo folder and end with code in a FINISH folder, implementing a single migration. Upon completion, users should confirm their code (for the most part) matches what's in the FINISH folder. The baseline migration sample app (Module 0; link below) is a barebones Python 2.7 App Engine app that uses the `webapp2` web framework plus the `ndb` Datastore library.

1. With _Module 0_ as the STARTing point, the Module 1 codelab migrates from the `webapp2` web framework to Flask, FINISHing at code matching the _Module 1_ repo.
1. Next, STARTing with the _Module 1_ application code (yours or ours), _Module 2_ migrates from  `ndb` to Cloud NDB, ending with code matching the (Module 2) FINISH repo folder. There's also has a bonus migration to Python 3, resulting in another FINISH repo folder, this one deployed on the next-generation platform.
1. _Your_ Python 2 apps may be using other built-in services like Task Queues or Memcache, so additional migration modules follow, some more optional than others, and not all are available yet (keep checking back here for updates).

### The order of migrations

Beyond Module 2, with some exceptions, **there is no specific order** of what migrations modules to tackle next. It depends on your needs (and your applications'). However, there are related migrations where one or more modules must be completed beforehand. This table attempts to put an order on module subsets.

Topic | Module ordering | Description
--- | --- | ---
Baseline | 0 &rArr; 1 | Not a migration but a description of the baseline application (review this material before doing any migrations)
Web framework | 1 &rArr; _everything else_ | Current App Engine runtimes do not come with a web framework, so this must be the first migration performed. All migrations below can be performed after this one.
Bundled services | 17 and 22 | These modules are for those who want to continue using Python bundled services from Python 3 App Engine.
Datastore | 2 [&rArr; 3 [&rArr; 6]] | Moving off App Engine `ndb` makes your apps more portable, so the **Module 2** Cloud NDB migration is _recommended_. **Module 3:** Migrating to Cloud Datastore (Firestore in Datastore mode) is _optional_ and only recommended if you have other code using Cloud Datastore. **Module 6**: Migrating to Cloud Firestore (Native mode) is generally _not recommended_ unless you must have the Firebase features it has, and those features will eventually be integrated into Cloud Datastore.
(Push) Task Queues | [7 &rArr;] 8 [&rArr; 9] | Moving off App Engine `taskqueue` makes your apps more portable, so the **Module 8** Cloud Tasks migration is _recommended_ for those using push tasks. Those unfamiliar with push tasks should do **Module 7** first to add push tasks to the sample app. **Module 9:** Migrating to Cloud Datastore (Firestore in Datastore mode), Cloud Tasks (v2), and Python 3 is _optional_ and only recommended if you have other code using Cloud Datastore and considering upgrading to Python 3.
(Pull) Task Queues | [18 &rArr;] 19 | Moving off App Engine `taskqueue` makes your apps more portable, so the **Module 19** Cloud Pub/Sub migration is _recommended_ for those using pull tasks. The app is also ported to Python 3. Those unfamiliar with pull tasks should do **Module 18** first to add pull tasks to the sample app.
Memcache | [12 &rArr;] 13 | Moving off App Engine `memcache` makes your apps more portable, so the **Module 13** Cloud Memorystore (for Redis) migration is _recommended_ for those using `memcache`. Those unfamiliar with `memcache` should do **Module 12** first to add its usage to the sample app.
Cloud Functions | 11 | Cloud Functions does not support Python 2, so after the Module 1 migration, you need to upgrade your app to Python 3 before attempting this migration, recommended if you have a very small App Engine app, or it has only one function/feature.
Cloud Run | 4 or 5 | **Module 4** covers migrating to Cloud Run with Docker. Those unfamiliar with containers or do not wish to create/maintain a `Dockerfile` should do **Module 5**. Those doing **Module 4** will get additional information about Cloud Run in **Module 5** not covered in **Module 4**.
Blobstore | [15 &rArr;] 16 | Moving off App Engine `blobstore` makes your apps more portable, so the **Module 16** Cloud Storage migration is _recommended_ for those using `blobstore`. Those unfamiliar with `blobstore` should do **Module 15** first to add its usage to the sample app.
Users | [20 &rArr;] 21 | Moving off App Engine `users` makes your apps more portable, so the **Module 21** Cloud Identity Platform migration is _recommended_ for those using `users`. Those unfamiliar with `users` should do **Module 20** first to add its usage to the sample app.
General migration | 6 &rArr; 10 &rArr; 14 | This series is more generic and not targeting a specific feature migration, but rather if you need to migrate your App Engine apps from one running project to another. It starts with **Module 6** if you need to migrate your code, say from Datastore to Firestore. **Module 10** is if you need to migrate your data from one project to another, and finally, **Module 14** is after you're done migrating your app, your data, or both, and need to migrate a running service on one GCP project to another.


## Migration modules

The table below summarizes migration module resources currently available along with a more detailed table of contents below. Be sure to check back for updates as more resources are planned.


### Summary table

Module | Topic | Video | Codelab | START here | FINISH here
--- | --- | --- | --- | --- | ---
0 | Baseline app| [link](https://developers.googleblog.com/2021/06/introducing-serverless-migration.html?utm_source=blog&utm_medium=partner&utm_campaign=CDR_wes_aap-serverless_smsintro_201023)| _N/A_ (no tutorial; just review the code) | _N/A_ | Module 0 [code](/mod0-baseline) (2.x)
1 | Migrate to Flask | [link](https://developers.googleblog.com/2021/07/migrating-from-app-engine-webapp2-to-flask.html?utm_source=blog&utm_medium=partner&utm_campaign=CDR_wes_aap-serverless_mgrwa2flsk_201008)| [link](https://codelabs.developers.google.com/codelabs/cloud-gae-python-migrate-1-flask?utm_source=codelabs&utm_medium=et&utm_campaign=CDR_wes_aap-serverless_mgrwa2flsk_201008&utm_content=-) | Module 0 [code](/mod0-baseline) (2.x) | Module 1 [code](/mod1-flask) (2.x) (and [code](/mod1b-flask) (3.x))
2 | Migrate to Cloud NDB | [link](https://developers.googleblog.com/2021/07/migrating-from-app-engine-ndb-to-cloud-ndb.html?utm_source=blog&utm_medium=partner&utm_campaign=CDR_wes_aap-serverless_mgrcloudndb_201021)| [link](https://codelabs.developers.google.com/codelabs/cloud-gae-python-migrate-2-cloudndb?utm_source=codelabs&utm_medium=et&utm_campaign=CDR_wes_aap-serverless_mgrcloudndb_201021&utm_content=-) | Module 1 [code](/mod1-flask) (2.x) | Module 2 [code](/mod2a-cloudndb) (2.x) &amp; [code](/mod2b-cloudndb) (3.x)
3 | Migrate to Cloud Datastore | [link](https://developers.googleblog.com/2021/08/cloud-ndb-to-cloud-datastore-migration.html?utm_source=blog&utm_medium=partner&utm_campaign=CDR_wes_aap-serverless_mgrcloudds_201003) | [link](https://codelabs.developers.google.com/codelabs/cloud-gae-python-migrate-3-datastore?utm_source=codelabs&utm_medium=et&utm_campaign=CDR_wes_aap-serverless_mgrcloudds_201003&utm_content=-) | Module 2 [code](/mod2a-cloudndb) (2.x) &amp; [code](/mod2b-cloudndb) (3.x) | Module 3 [code](/mod3a-datastore) (2.x) &amp; [code](/mod3b-datastore) (3.x)
4 | Migrate to Cloud Run with Docker | [link](https://developers.googleblog.com/2021/08/containerizing-google-app-engine-apps-for-cloud-run.html?utm_source=blog&utm_medium=partner&utm_campaign=CDR_wes_aap-serverless_mgrcrdckr_sms_201017) | [link](https://codelabs.developers.google.com/codelabs/cloud-gae-python-migrate-4-rundocker?utm_source=codelabs&utm_medium=et&utm_campaign=CDR_wes_aap-serverless_mgrcrdckr_sms_201017&utm_content=-) | Module 2 [code](/mod2a-cloudndb) (2.x) &amp; Module 3 [code](/mod3b-datastore) (3.x) | Module 4 [code](/mod4a-rundocker) (2.x) &amp; [code](/mod4b-rundocker) (3.x)
5 | Migrate to Cloud Run with Buildpacks | [link](https://developers.googleblog.com/2021/09/an-easier-way-to-move-your-app-engine-to-cloud-run.html?utm_source=blog&utm_medium=partner&utm_campaign=CDR_wes_aap-serverless_mgrcrbdpk_sms_201031) | [link](https://codelabs.developers.google.com/codelabs/cloud-gae-python-migrate-5-runbldpks?utm_source=codelabs&utm_medium=et&utm_campaign=CDR_wes_aap-serverless_mgrcrbdpk_sms_201031&utm_content=-) | Module 2 [code](/mod2b-cloudndb) (3.x) | Module 5 [code](/mod5-runbldpks) (3.x)
6 | Migrate to Cloud Firestore | _N/A_ | _N/A_ | Module 3 [code](/mod3b-datastore) (3.x) | _no work required; [Datastore upgrade automatic](https://cloud.google.com/datastore/docs/upgrade-to-firestore)_
7 | Add App Engine `taskqueue` push tasks | [link](https://developers.googleblog.com/2021/09/how-to-use-app-engine-push-queues-in.html?utm_source=blog&utm_medium=partner&utm_campaign=CDR_wes_aap-serverless_mgrgaetasks_sms_201028) | [link](https://codelabs.developers.google.com/codelabs/cloud-gae-python-migrate-7-gaetasks?utm_source=codelabs&utm_medium=et&utm_campaign=CDR_wes_aap-serverless_mgrgaetasks_sms_201028&utm_content=-) | Module 1 [code](/mod1-flask) (2.x) | Module 7 [code](/mod7-gaetasks) (2.x) &amp; [code](/mod7b-gaetasks) (3.x)
8 | Migrate to Cloud Tasks | [link](https://developers.googleblog.com/2021/10/migrating-app-engine-push-queues-to.html?utm_source=blog&utm_medium=partner&utm_campaign=CDR_wes_aap-serverless_mgrcloudtasks_sms_201112) | [link](https://codelabs.developers.google.com/codelabs/cloud-gae-python-migrate-8-cloudtasks?utm_source=codelabs&utm_medium=et&utm_campaign=CDR_wes_aap-serverless_mgrcloudtasks_sms_201112&utm_content=-) | Module 7 [code](/mod7-gaetasks) (2.x) | Module 8 [code](/mod8-cloudtasks) (2.x)
9 | Migrate to Python 3, Cloud Datastore &amp; Cloud Tasks v2 | _TBD_ | [link](https://codelabs.developers.google.com/codelabs/cloud-gae-python-migrate-9-py3dstasks?utm_source=codelabs&utm_medium=et&utm_campaign=CDR_wes_aap-serverless_mgrpy3fstasks_sms_201126&utm_content=-) | Module 8 [code](/mod8-cloudtasks) (2.x) | Module 9 [code](/mod9-py3dstasks)
10 | Migrate Datastore/Firestore data to another project | _TBD_ | _N/A_ | _N/A_ | _TBD_
11 | Migrate to Cloud Functions | [link](https://developers.googleblog.com/2022/04/how-can-app-engine-users-take-advantage-of-cloud-functions.html?utm_source=blog&utm_medium=partner&utm_campaign=CDR_wes_aap-serverless_mgrcloudfuncs_sms_202006) | [link](https://codelabs.developers.google.com/codelabs/cloud-gae-python-migrate-11-functions?utm_source=codelabs&utm_medium=et&utm_campaign=CDR_wes_aap-serverless_mgrcloudfuncs_sms_202006&utm_content=-) | Module 2 [code](/mod2b-cloudndb) (3.x) | Module 11 [code](/mod11-functions) (3.x)
12 | Add App Engine `memcache` | [link](https://developers.googleblog.com/2022/05/how-to-use-app-engine-memcache-in-flask-apps.html?utm_source=blog&utm_medium=partner&utm_campaign=CDR_wes_aap-serverless_mgrmemcache_sms_202006) | [link](https://codelabs.developers.google.com/codelabs/cloud-gae-python-migrate-12-memcache?utm_source=codelabs&utm_medium=et&utm_campaign=CDR_wes_aap-serverless_mgrmemcache_sms_202006&utm_content=-) | Module 1 [code](/mod1-flask) (2.x) | Module 12 [code](/mod12-memcache) (2.x) &amp; [code](/mod12b-memcache) (3.x)
13 | Migrate to Cloud Memorystore | [link](https://developers.googleblog.com/2022/06/Migrating-from-App-Engine-Memcache-to-Cloud-Memorystore-Module-13.html?utm_source=blog&utm_medium=partner&utm_campaign=CDR_wes_aap-serverless_mgrmemorystore_sms_202029) | [link](https://codelabs.developers.google.com/codelabs/cloud-gae-python-migrate-13-memorystore?utm_source=codelabs&utm_medium=et&utm_campaign=CDR_wes_aap-serverless_mgrmemorystore_sms_202029&utm_content=-) | Module 12 [code](/mod12-memcache) (2.x) &amp; [code](/mod12b-memcache) (3.x) | Module 13 [code](/mod13a-memorystore) (2.x) &amp; [code](/mod13b-memorystore) (3.x)
14 | Migrate service between projects | _TBD_ | _TBD_ | _TBD_ | _TBD_
15 | Add App Engine `blobstore` | [link](https://developers.googleblog.com/2022/07/how-to-use-app-engine-blobstore-Module15.html?utm_source=blog&utm_medium=partner&utm_campaign=CDR_wes_aap-serverless_mgrblobstore_sms_202029) | [link](https://codelabs.developers.google.com/codelabs/cloud-gae-python-migrate-15-blobstore?utm_source=codelabs&utm_medium=et&utm_campaign=CDR_wes_aap-serverless_mgrblobstore_sms_202029&utm_content=-) | Module 0 [code](/mod0-baseline) (2.x) | Module 15 [code](/mod15-blobstore) (2.x)
16 | Migrate to Cloud Storage | [link](https://developers.googleblog.com/2022/08/migrating-from-app-engine-blobstore-to-cloud-storage-module-16.html?utm_source=blog&utm_medium=partner&utm_campaign=CDR_wes_aap-serverless_mgrcloudstorage_sms_202029) | [link](https://codelabs.developers.google.com/codelabs/cloud-gae-python-migrate-16-cloudstorage?utm_source=codelabs&utm_medium=et&utm_campaign=CDR_wes_aap-serverless_mgrcloudstorage_sms_202029&utm_content=-) | Module 15 [code](/mod15-blobstore) (2.x) | Module 16 [code](/mod16-cloudstorage) (2.x & 3.x)
17 | Migrate to Python 3 bundled services (Part 1) | [link](https://developers.googleblog.com/2022/10/extending-support-for-app-engine-bundled-services-module-17.html?utm_source=blog&utm_medium=partner&utm_campaign=CDR_wes_aap-serverless_mgrwormhole_sms_202002) | [link](http://codelabs.developers.google.com/codelabs/cloud-gae-python-migrate-17-bundled?utm_source=codelabs&utm_medium=et&utm_campaign=CDR_wes_aap-serverless_mgrwormhole_sms_202002&utm_content=-) | Module 1 [code](/mod1-flask) (2.x) | Module 1 [code](/mod1b-flask) (3.x)
18 | Add App Engine `taskqueue` pull tasks | [link](https://developers.googleblog.com/2022/11/how-to-use-app-engine-pull-tasks-module-18.html?utm_source=blog&utm_medium=partner&utm_campaign=CDR_wes_aap-serverless_mgrgaepull_sms_202013) | [link](https://codelabs.developers.google.com/codelabs/cloud-gae-python-migrate-18-gaepull?utm_source=codelabs&utm_medium=et&utm_campaign=CDR_wes_aap-serverless_mgrgaepull_sms_202013&utm_content=-) | Module 1 [code](/mod1-flask) (2.x) | Module 18 [code](/mod18-gaepull) (2.x)
19 | Migrate to Cloud Pub/Sub | [link](https://developers.googleblog.com/2022/12/migrating-from-app-engine-pull-tasks-to.html?utm_source=blog&utm_medium=partner&utm_campaign=CDR_wes_aap-serverless_mgrpubsub_sms_202016) | [link](https://codelabs.developers.google.com/codelabs/cloud-gae-python-migrate-19-pubsub?utm_source=codelabs&utm_medium=et&utm_campaign=CDR_wes_aap-serverless_mgrpubsub_sms_202016&utm_content=-) | Module 18 [code](/mod18-gaepull) (2.x) | Module 19 [code](/mod19-pubsub) (2.x & 3.x)
20 | Add App Engine `users` | [link](https://developers.googleblog.com/2022/12/how-to-use-app-engine-users-service-module-20.html?utm_source=blog&utm_medium=partner&utm_campaign=CDR_wes_aap-serverless_mgrgaeusers_sms_202119) | [link](https://codelabs.developers.google.com/codelabs/cloud-gae-python-migrate-20-gaeusers?utm_source=codelabs&utm_medium=et&utm_campaign=CDR_wes_aap-serverless_mgrgaeusers_sms_202119&utm_content=-)| Module 1 [code](/mod1-flask) (2.x) | Module 20 [code](/mod20-gaeusers) (2.x)
21 | Migrate to Cloud Identity Platform | [link](https://developers.googleblog.com/2023/01/migrating-from-app-engine-users-to-cloud-identity-module-21.html?utm_source=blog&utm_medium=partner&utm_campaign=CDR_wes_aap-serverless_mgridenplat_sms_202119) | [link](https://codelabs.developers.google.com/codelabs/cloud-gae-python-migrate-21-idenplat?utm_source=codelabs&utm_medium=et&utm_campaign=CDR_wes_aap-serverless_mgridenplat_sms_202119&utm_content=-)| Module 20 [code](/mod20-gaeusers) (2.x) |  Module 21 [code](/mod21a-idenplat) (2.x) &amp; [code](/mod21b-idenplat) (3.x)
22 | Migrate to Python 3 bundled services (Part 2) | [link](http://youtu.be/ZhEBSvnz_BQ?list=PL2pQQBHvYcs0PEecTcLD9_VaLvuhK0_VQ&utm_source=youtube&utm_medium=unpaidsoc&utm_campaign=CDR_wes_aap-serverless_mgrwormhole2_sms_202002&utm_content=info_card) | _N/A_ | Module 22  [code](/mod22-bundled) (2.x & 3.x) | _(&lArr; same folder)_


### Table of contents

If there is a logical codelab to do immediately after completing one, they will be designated as NEXT. Other recommended codelabs will be listed as RECOMMENDED, and the more optional ones will be labeled as OTHERS (and usually in some kind of priority order).


#### Migrations from legacy App Engine APIs/bundled services

- [Module 1 codelab](https://codelabs.developers.google.com/codelabs/cloud-gae-python-migrate-1-flask?utm_source=codelabs&utm_medium=et&utm_campaign=CDR_wes_aap-serverless_mgrwa2flsk_201008&utm_content=-): **Migrate from `webapp2` to [Flask](https://flask.palletsprojects.com)**
    - **Required** migration (can also pick your own framework)
        - `webapp2` does not do routing thus unsupported by App Engine (even though a [3.x port exists](https://github.com/fili/webapp2-gae-python37))
    - Python 2
        - START:  [Module 0 code - Baseline](/mod0-baseline)
        - FINISH: [Module 1 code - Framework](/mod1-flask)
    - NEXT:
        - Module 2 - migrate from App Engine NDB to Cloud NDB (for Datastore access)

- [Module 2 codelab](https://codelabs.developers.google.com/codelabs/cloud-gae-python-migrate-2-cloudndb?utm_source=codelabs&utm_medium=et&utm_campaign=CDR_wes_aap-serverless_mgrcloudndb_201021&utm_content=-): **Migrate from App Engine `ndb` to [Cloud NDB](https://googleapis.dev/python/python-ndb/latest)**
    - Python 2
        - START:  [Module 1 code - Framework](/mod1-flask)
        - FINISH: [Module 2 code - Cloud NDB](/mod2a-cloudndb)
    - Codelab bonus port to Python 3.x
        - FINISH: [Module 2 code - Cloud NDB](/mod2b-cloudndb) (3.x)
    - RECOMMENDED:
        - Module 7 - add App Engine Task Queue push tasks (and migrate to Cloud Tasks in Module 8)
        - Module 18 - add App Engine Task Queue pull tasks (and migrate to Cloud Pub/Sub in Module 19)
        - Module 12 - add App Engine Memcache (and migrate to Cloud Memorystore in Module 13)
        - Module 15 - add App Engine Blobstore (and migrate to Cloud Storage in Module 16)
        - Module 20 - add App Engine Users (and migrate to Cloud Identity Platform in Module 21)

- [Module 7 codelab](https://codelabs.developers.google.com/codelabs/cloud-gae-python-migrate-7-gaetasks?utm_source=codelabs&utm_medium=et&utm_campaign=CDR_wes_aap-serverless_mgrgaetasks_sms_201028&utm_content=-): **Add App Engine Task Queues push tasks to existing sample app**
    - **Not a migration**: add GAE Task Queues to prepare for migration to Cloud Tasks
    - Python 2
        - START:  [Module 1 code - Framework](/mod1-flask)
        - FINISH: [Module 7 code - GAE Task Queue push tasks](/mod7-gaetasks)
    - NEXT:
        - Module 8 - migrate App Engine Task Queue push tasks to Cloud Tasks

- [Module 8 codelab](https://codelabs.developers.google.com/codelabs/cloud-gae-python-migrate-8-cloudtasks?utm_source=codelabs&utm_medium=et&utm_campaign=CDR_wes_aap-serverless_mgrcloudtasks_sms_201112&utm_content=-): **Migrate from App Engine Task Queues push tasks to [Cloud Tasks](http://cloud.google.com/tasks) v1**
    - Python 2
        - START:  [Module 7 code - GAE Task Queue push tasks](/mod7-gaetasks)
        - FINISH: [Module 8 code - Cloud Tasks](/mod8-cloudtasks)
    - RECOMMENDED:
        - Module 9 - migrate to Python 3 and Cloud Datastore
        - Module 18 - add App Engine Task Queue pull tasks (and migrate to Cloud Pub/Sub in Module 19)
        - Module 12 - add App Engine Memcache (and migrate to Cloud Memorystore in Module 13)
        - Module 15 - add App Engine Blobstore (and migrate to Cloud Storage in Module 16)
        - Module 20 - add App Engine Users (and migrate to Cloud Identity Platform in Module 21)

- [Module 9 codelab](https://codelabs.developers.google.com/codelabs/cloud-gae-python-migrate-9-py3dstasks?utm_source=codelabs&utm_medium=et&utm_campaign=CDR_wes_aap-serverless_mgrpy3fstasks_sms_201126&utm_content=-): **Migrate a Python 2 Cloud NDB &amp; Cloud Tasks (v1) app to a Python 3 Cloud Datastore &amp; Cloud Tasks (v2) app**
    - **Optional** migrations
        - Migrating to Python 3 is not required but recommended as [Python 2 has been sunset](http://python.org/doc/sunset-python-2)
        - Migrating to Cloud Datastore is optional as Cloud NDB works on 3.x
    - Python 2
        - START:  [Module 8 code - Cloud Tasks](/mod8-cloudtasks)
    - Python 3
        - FINISH: _TBD_
    - RECOMMENDED:
        - Module 18 - add App Engine Task Queue pull tasks (and migrate to Cloud Pub/Sub in Module 19)
        - Module 12 - add App Engine Memcache (and migrate to Cloud Memorystore in Module 13)
        - Module 15 - add App Engine Blobstore (and migrate to Cloud Storage in Module 16)
        - Module 20 - add App Engine Users (and migrate to Cloud Identity Platform in Module 21)

- [Module 18 codelab](https://codelabs.developers.google.com/codelabs/cloud-gae-python-migrate-18-gaepull?utm_source=codelabs&utm_medium=et&utm_campaign=CDR_wes_aap-serverless_mgrgaepull_sms_202013&utm_content=-): **Add App Engine Task Queues pull tasks to existing sample app**
    - **Not a migration**: add GAE Task Queues to prepare for migration to Cloud Tasks
    - Python 2
        - START:  [Module 1 code - Framework](/mod1-flask)
        - FINISH: [Module 18 code - GAE Task Queue pull tasks](/mod18-gaepull)
    - NEXT: Module 19 - migrate App Engine pull tasks to Cloud Pub/Sub

- [Module 19 codelab](https://codelabs.developers.google.com/codelabs/cloud-gae-python-migrate-19-pubsub?utm_source=codelabs&utm_medium=et&utm_campaign=CDR_wes_aap-serverless_mgrpubsub_sms_202016&utm_content=-): **Migrate from App Engine Task Queues pull tasks to [Cloud Pub/Sub](http://cloud.google.com/pubsub)**
    - Python 2
        - START:  [Module 18 code - GAE Task Queue pull tasks](/mod18-gaepull)
    - Python 3
        - FINISH: [Module 19 code - Cloud Pub/Sub](/mod19-pubsub)
    - RECOMMENDED:
        - Module 7 - add App Engine Task Queue push tasks (and migrate to Cloud Tasks in Module 8)
        - Module 12 - add App Engine Memcache (and migrate to Cloud Memorystore in Module 13)
        - Module 15 - add App Engine Blobstore (and migrate to Cloud Storage in Module 16)
        - Module 20 - add App Engine `users` (and migrate to Cloud Identity Platform in Module 21)

- [Module 12 codelab](https://codelabs.developers.google.com/codelabs/cloud-gae-python-migrate-12-memcache?utm_source=codelabs&utm_medium=et&utm_campaign=CDR_wes_aap-serverless_mgrmemcache_sms_202006&utm_content=-): **Add App Engine Memcache to existing sample app**
    - **Not a migration**: add GAE Memcache to prepare for migration to Cloud Memorystore
    - Python 2
        - START:  [Module 1 code - Framework](/mod1-flask)
        - FINISH: [Module 12 code - GAE Memcache](/mod12-memcache)
    - NEXT: Module 13 - migrate App Engine Memcache to Cloud Memorystore

- [Module 13 codelab](https://codelabs.developers.google.com/codelabs/cloud-gae-python-migrate-13-memorystore?utm_source=codelabs&utm_medium=et&utm_campaign=CDR_wes_aap-serverless_mgrmemorystore_sms_202029&utm_content=-): **Migrate from App Engine Memcache to [Cloud Memorystore (for Redis)](http://cloud.google.com/memorystore) v1**
    - Python 2
        - START:  [Module 12 code - GAE Memcache](/mod12-memcache)
        - FINISH: [Module 13 code - Cloud Tasks](/mod13a-memorystore)
    - Python 3
        - FINISH: [Module 13 code - Cloud Tasks](/mod13b-memorystore)
    - RECOMMENDED:
        - Module 7 - add App Engine Task Queue push tasks (and migrate to Cloud Tasks in Module 8)
        - Module 18 - add App Engine Task Queue pull tasks (and migrate to Cloud Pub/Sub in Module 19)
        - Module 15 - add App Engine Blobstore (and migrate to Cloud Storage in Module 16)
        - Module 20 - add App Engine `users` (and migrate to Cloud Identity Platform in Module 21)

- [Module 15 codelab](https://codelabs.developers.google.com/codelabs/cloud-gae-python-migrate-12-memcache?utm_source=codelabs&utm_medium=et&utm_campaign=CDR_wes_aap-serverless_mgrmemcache_sms_202006&utm_content=-): **Add App Engine Blobstore to existing sample app**
    - **Not a migration**: add GAE Blobstore to prepare for migration to Cloud Storage
    - Python 2
        - START:  [Module 0 code - Baseline](/mod0-baseline)
        - FINISH: [Module 15 code - GAE Blobstore](/mod15-blobstore)
    - NEXT: Module 16 - migrate App Engine Blobstore to Cloud Storage

- [Module 16 codelab](https://codelabs.developers.google.com/codelabs/cloud-gae-python-migrate-13-memorystore?utm_source=codelabs&utm_medium=et&utm_campaign=CDR_wes_aap-serverless_mgrmemorystore_sms_202029&utm_content=-): **Migrate from App Engine Blobstore to [Cloud Storage (for Redis)](http://cloud.google.com/storage) v1**
    - Python 2
        - START:  [Module 15 code - GAE Blobstore](/mod15-blobstore)
        - FINISH: [Module 16 code - Cloud Storage](/mod16-cloudstorage)
    - Python 3
        - FINISH: [Module 16 code - Cloud Storage](/mod16-cloudstorage) (_same as Python 2 version_)
    - RECOMMENDED:
        - Module 7 - add App Engine Task Queue push tasks (and migrate to Cloud Tasks in Module 8)
        - Module 18 - add App Engine Task Queue pull tasks (and migrate to Cloud Pub/Sub in Module 19)
        - Module 12 - add App Engine Memcache (and migrate to Cloud Memorystore in Module 13)
        - Module 20 - add App Engine Users (and migrate to Cloud Identity Platform in Module 21)

- [Module 20 codelab](https://codelabs.developers.google.com/codelabs/cloud-gae-python-migrate-20-gaeusers?utm_source=codelabs&utm_medium=et&utm_campaign=CDR_wes_aap-serverless_mgrgaeusers_sms_202119&utm_content=-): **Add App Engine Users to existing sample app**
    - **Not a migration**: add GAE Users to prepare for migration to Cloud Identity Platform/Firebase Auth
    - Python 2
        - START:  [Module 1 code - Framework](/mod1-flask)
        - FINISH: [Module 20 code - GAE Users](/mod20-gaeusers)
    - NEXT:
        - Module 21 - migrate App Engine Users to Cloud Identity Platform/Firebase Auth

- [Module 21 codelab](https://codelabs.developers.google.com/codelabs/cloud-gae-python-migrate-21-idenplat?utm_source=codelabs&utm_medium=et&utm_campaign=CDR_wes_aap-serverless_mgridenplat_sms_202119&utm_content=-): **Migrate from App Engine Users to [Cloud Identity Platform](http://cloud.google.com/identity-platform)/Firebase Auth**
    - Python 2
        - START:  [Module 20 code - GAE Users](/mod20-gaeusers)
        - FINISH: [Module 21 code - Cloud Identity Platform](/mod21a-idenplat)/Firebase Auth
    - Python 3
        - FINISH: [Module 21 code - Cloud Identity Platform](/mod21b-idenplat)/Firebase Auth
    - RECOMMENDED:
        - Module 7 - add App Engine Task Queue push tasks (and migrate to Cloud Tasks in Module 8)
        - Module 18 - add App Engine Task Queue pull tasks (and migrate to Cloud Pub/Sub in Module 19)
        - Module 12 - add App Engine Memcache (and migrate to Cloud Memorystore in Module 13)
        - Module 15 - add App Engine Blobstore (and migrate to Cloud Storage in Module 16)


- [Module 3 codelab](https://codelabs.developers.google.com/codelabs/cloud-gae-python-migrate-3-datastore?utm_source=codelabs&utm_medium=et&utm_campaign=CDR_wes_aap-serverless_mgrcloudds_201003&utm_content=-): **Migrate from Cloud NDB to [Cloud Datastore](http://cloud.google.com/datastore)**
    - **Optional** migration
        - Recommended only if using Cloud Datastore elsewhere (GAE *or* non-App Engine) apps
        - Helps w/code consistency &amp; reusability, reduces maintenance costs
    - Python 2
        - START:  [Module 2 code - Cloud NDB](/mod2a-cloudndb)
        - FINISH: [Module 3 code - Cloud Datastore](/mod3a-datastore)
    - Python 3
        - START:  [Module 2 code - Cloud NDB](/mod2b-cloudndb)
        - FINISH: [Module 3 code - Cloud Datastore](/mod3b-datastore)
    - RECOMMENDED:
        - Module 7 - add App Engine Task Queue push tasks (and migrate to Cloud Tasks in Module 8)
        - Module 18 - add App Engine Task Queue pull tasks (and migrate to Cloud Pub/Sub in Module 19)
        - Module 12 - add App Engine Memcache (and migrate to Cloud Memorystore in Module 13)
        - Module 15 - add App Engine Blobstore (and migrate to Cloud Storage in Module 16)
        - Module 20 - add App Engine Users (and migrate to Cloud Identity Platform in Module 21)


#### Migrations to other Cloud serverless platforms

- [Module 4 codelab](https://codelabs.developers.google.com/codelabs/cloud-gae-python-migrate-4-rundocker?utm_source=codelabs&utm_medium=et&utm_campaign=CDR_wes_aap-serverless_mgrcrdckr_sms_201017&utm_content=-): **Migrate from App Engine to Cloud Run with Docker**
    - **Optional** migration
        - "Containerize" your app (migrate your app to a container) with Docker
    - Python 2
        - START:  [Module 2 code - Cloud NDB](/mod2a-cloudndb)
        - FINISH: [Module 4 code - Cloud Run - Docker 3.x](/mod4a-rundocker)
    - Python 3
        - START:  [Module 3 code - Cloud Datastore](/mod3b-datastore)
        - FINISH: [Module 4 code - Cloud Run - Docker](/mod4b-rundocker)
    - RECOMMENDED:
        - Module 5 - migrate to Cloud Run container with Cloud Buildpacks
        - Module 11 - migrate to Cloud Functions

- [Module 5 codelab](https://codelabs.developers.google.com/codelabs/cloud-gae-python-migrate-5-runbldpks?utm_source=codelabs&utm_medium=et&utm_campaign=CDR_wes_aap-serverless_mgrcrbdpk_sms_201031&utm_content=-): **Migrate from App Engine to Cloud Run with Cloud Buildpacks**
    - **Optional** migration
        - "Containerize" your app (migrate your app to a container) with...
        - [Cloud Buildpacks]() which lets you containerize your app without `Dockerfile`s
    - Python 3 only
        - START:  [Module 2 code - Cloud NDB](/mod2b-cloudndb)
        - FINISH: [Module 5 code - Cloud Run - Buildpacks 3.x](/mod5-runbldpks)
    - RECOMMENDED:
        - Module 4 - migrate to Cloud Run container with Docker
        - Module 11 - migrate to Cloud Functions

- [Module 11 codelab](https://codelabs.developers.google.com/codelabs/cloud-gae-python-migrate-11-functions?utm_source=codelabs&utm_medium=et&utm_campaign=CDR_wes_aap-serverless_mgrcloudfuncs_sms_202006&utm_content=-): **Migrate from App Engine to Cloud Functions**
    - **Optional** migration
        - Recommended for small apps or for breaking up large apps into multiple microservices
    - Python 3 only
        - START:  [Module 2 code - Cloud NDB](/mod2b-cloudndb)
        - FINISH: [Module 11 code - Cloud Functions](/mod11-functions)
    - RECOMMENDED:
        - Module 7 - add App Engine Task Queue push tasks (and migrate to Cloud Tasks in Module 8)
        - Module 18 - add App Engine Task Queue pull tasks (and migrate to Cloud Pub/Sub in Module 19)
        - Module 12 - add App Engine `memcache` (and migrate to Cloud Memorystore in Module 13)
        - Module 15 - add App Engine `blobstore` (and migrate to Cloud Storage in Module 16)
    - OTHER OPTIONS (in somewhat priority order):
        - Module 5 - migrate to Cloud Run container with Cloud Buildpacks


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

Many legacy App Engine first generation platform (Python 2, Java 8, PHP 5, and Go 1.11 &amp; older) services are available ([as of Sep 2021](https://cloud.google.com/blog/products/serverless/support-for-app-engine-services-in-second-generation-runtimes) for second generation runtimes (Python 3, Java 11/17, PHP 7/8, and Go 1.12 &amp; newer) in a public preview. There are no videos or codelabs yet, however the Module 1 Flask migration using App Engine `ndb` [Python 2 sample](/mod1-flask) is available in [Python 3](/mod1b-flask) if you have access. Similarly, Python 3 editions are also available for Modules 7 and 12 which add usage of App Engine `taskqueue` and `memcache`, respectively. Also see the [documentation on accessing bundled services from Python 3](https://cloud.google.com/appengine/docs/standard/python3/services/access).


## Community

Python App Engine developers hang out in various online communities, including these:
- [Slack](https://googlecloud-community.slack.com) (`#app-engine`, `#python`, and other channels); visit [this link](https://join.slack.com/t/googlecloud-community/shared_invite/zt-ywj8ieuc-BrAaHC~qe5IgelXS9vzNRA) to join
- [Reddit](http://reddit.com) in the [Google Cloud](https://reddit.com/googlecloud) or [App Engine](https://reddit.com/appengine) subs (subReddits).
- [App Engine mailing list](http://groups.google.com/group/google-appengine)


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
