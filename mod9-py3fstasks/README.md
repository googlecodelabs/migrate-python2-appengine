# Module 9 - Migrate from Python 2 to 3 and Cloud NDB to Cloud Firestore

This repo folder is the corresponding Python 3 code to the [Module 9 codelab](http://g.co/codelabs/pae-migrate-py3fstasks). The tutorial STARTs with the Python 2 code in the [Module 8 repo folder](/mod7-cloudtasks) and leads developers through migrating from Python 2 to 3, Cloud NDB to Cloud Firestore (skipping over a Cloud Datstore migration) plus any changes from Cloud Tasks v1 to v2, culminating in the code in this folder. One major addition to look for here vs. Module 8 is that App Engine `taskqueue` creates a `default` push queue while Cloud Tasks does not, so that now has to be done in code.

NOTE: The deletion process in this app is "one-at-a-time." If your app requires deletion of more than a few documents, consider switching to the batch model. In this case, you would replace `_delete_docs()` with:

    def _delete_docs(visits):
        'app-internal generator deleting old FS visit documents'
        batch = fs_client.batch()
        for visit in visits:
            batch.delete(visit.reference)
            yield visit.id
        batch.commit()
