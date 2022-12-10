# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from flask import Flask, abort, redirect, request
from google.appengine.api import wrap_wsgi_app
from google.appengine.ext import blobstore, ndb

UPLOAD_FORM = '''\
<title>Module 22 Blobstore sample app</title>
<h2>Upload photo:</h2>
<form action="%s" method="POST" enctype="multipart/form-data">
    <input type="file" name="file"><p></p><input type="submit">
</form>'''

app = Flask(__name__)
app.wsgi_app = wrap_wsgi_app(app.wsgi_app)


class PhotoUpload(ndb.Model):
    'PhotoUpload entity for registering a photo'
    blob_key = ndb.BlobKeyProperty()


class PhotoUploadHandler(blobstore.BlobstoreUploadHandler):
    'PhotoUploadHandler handles a photo upload (POST)'
    def post(self):
        uploads = self.get_uploads(request.environ)
        blob_id = uploads[0].key() if uploads else None
        PhotoUpload(blob_key=blob_id).put()
        return redirect('/view_photo/%s' % blob_id)

@app.route('/upload_photo', methods=['POST'])
def upload_photo():
    'call upload handler for upload (POST) request'
    return PhotoUploadHandler().post()


class ViewPhotoHandler(blobstore.BlobstoreDownloadHandler):
    'ViewPhotoHandler handles a photo view/download (GET)'
    def get(self, blob_key):
        if blobstore.get(blob_key):
            headers = self.send_blob(request.environ, blob_key)
            headers['Content-Type'] = None
            return '', headers
        abort(404)

@app.route('/view_photo/<photo_key>')
def view_photo(photo_key):
    'call download handler for view (GET) request'
    return ViewPhotoHandler().get(photo_key)


@app.route('/')
def upload_form():
    'display photo upload HTML form'
    return UPLOAD_FORM % blobstore.create_upload_url('/upload_photo')
