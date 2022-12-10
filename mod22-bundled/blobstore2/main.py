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

import webapp2
from google.appengine.ext import blobstore, ndb
from google.appengine.ext.webapp import blobstore_handlers

UPLOAD_FORM = '''\
<title>Module 22 Blobstore sample app</title>
<h2>Upload photo:</h2>
<form action="%s" method="POST" enctype="multipart/form-data">
    <input type="file" name="file"><p></p><input type="submit">
</form>'''


class PhotoUpload(ndb.Model):
    'PhotoUpload entity for registering a photo'
    blob_key = ndb.BlobKeyProperty()


class PhotoUploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    'PhotoUploadHandler handles a photo upload (POST)'
    def post(self):
        uploads = self.get_uploads()
        blob_id = uploads[0].key() if uploads else None
        PhotoUpload(blob_key=blob_id).put()
        self.redirect('/view_photo/%s' % blob_id)


class ViewPhotoHandler(blobstore_handlers.BlobstoreDownloadHandler):
    'ViewPhotoHandler handles a photo view/download (GET)'
    def get(self, blob_key):
        self.send_blob(blob_key) if blobstore.get(blob_key) else self.error(404)


class MainHandler(webapp2.RequestHandler):
    'main application (GET) handler'
    def get(self):
        self.response.write(
                UPLOAD_FORM % blobstore.create_upload_url('/upload_photo'))


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/upload_photo', PhotoUploadHandler),
    ('/view_photo/([^/]+)?', ViewPhotoHandler),
], debug=True)
