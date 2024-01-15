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

import io
from flask import Flask, abort, redirect, request
from google.appengine.api import wrap_wsgi_app
from google.appengine.ext import blobstore, ndb

app = Flask(__name__)
app.wsgi_app = wrap_wsgi_app(app.wsgi_app, use_deferred=True)


class Visit(ndb.Model):
    'Visit entity registers visitor IP address & timestamp'
    visitor   = ndb.StringProperty()
    timestamp = ndb.DateTimeProperty(auto_now_add=True)
    blob_key = ndb.BlobKeyProperty()


def store_visit(remote_addr, user_agent, upload_key):
    'create new Visit entity in Datastore'
    Visit(visitor='{}: {}'.format(remote_addr, user_agent),
            file_blob = upload_key).put()


def fetch_visits(limit):
    'get most recent visits'
    return Visit.query().order(-Visit.timestamp).fetch(limit)


class UploadHandler(blobstore.BlobstoreUploadHandler):
    'Upload blob (POST) handler'
    def post(self):
        uploads = self.get_uploads(request.environ)
        blob_id = uploads[0].key() if uploads else None
        store_visit(self.request.remote_addr, self.request.user_agent, blob_id)
        return redirect('/', code=307)

class ViewBlobHandler(blobstore.BlobstoreDownloadHandler):
    'view uploaded blob (GET) handler'
    def get(self, blob_key):
        if not blobstore.get(blob_key):
            return "Blobg key not found", 404
        else:
            headers = self.send_blob(request.environ, blob_key) 

        # Prevent Flask from setting a default content-type.
        # GAE sets it to a guessed type if the header is not set.
            headers['Content-Type'] = None
            return '', headers

@app.route('/view_photo/<photo_key>')
def view_photo(photo_key):
    """View photo given a key."""
    return ViewBlobHandler().get(photo_key)


@app.route('/upload_photo', methods=['POST'])
def upload_photo():
    """Upload handler called by blobstore when a blob is uploaded in the test."""
    return UploadHandler().post()

@app.route('/', methods=['GET', 'POST'])
def root():
    'main application (GET/POST) handler'
    context = {}
    if request.method == 'GET':
        context['upload_url'] = url_for('upload')
    else:
        context['visits'] = fetch_visits(10)
    return render_template('index.html', **context)