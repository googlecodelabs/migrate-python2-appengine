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
import logging

from flask import (Flask, abort, redirect, render_template,
        request, send_file, url_for)
from werkzeug.utils import secure_filename

import google.auth
from google.cloud import ndb, storage, exceptions

app = Flask(__name__)
ds_client = ndb.Client()
gcs_client = storage.Client()
_, PROJECT_ID = google.auth.default()
BUCKET = '%s.appspot.com' % PROJECT_ID


def store_blob(fname, media):
    blob = gcs_client.bucket(BUCKET).blob(fname)
    blob.upload_from_file(media, content_type=media.content_type)


class Visit(ndb.Model):
    'Visit entity registers visitor IP address & timestamp'
    visitor   = ndb.StringProperty()
    timestamp = ndb.DateTimeProperty(auto_now_add=True)
    file_blob = ndb.BlobKeyProperty()  # backwards-compatibility
    file_gcs  = ndb.StringProperty()


def store_visit(remote_addr, user_agent, upload_key):
    'create new Visit entity in Datastore'
    with ds_client.context():
        Visit(visitor='{}: {}'.format(remote_addr, user_agent),
                file_gcs=upload_key).put()


def fetch_visits(limit):
    'get most recent visits'
    with ds_client.context():
        return Visit.query().order(-Visit.timestamp).fetch(limit)


@app.route('/upload', methods=['POST'])
def upload():
    'Upload blob (POST) handler'
    fname = None
    uploaded_file = request.files.get('file', None)
    if uploaded_file:
        fname = secure_filename(uploaded_file.filename)
        store_blob(fname, uploaded_file)
    store_visit(request.remote_addr, request.user_agent, fname)
    return redirect(url_for('root'), code=307)


@app.route('/view/<path:fname>')
def view(fname):
    'view uploaded blob (GET) handler'
    blob = gcs_client.bucket(BUCKET).blob(fname)
    try:
        media = blob.download_as_bytes()
    except exceptions.NotFound as e:
        abort(404)
    return send_file(io.BytesIO(media), mimetype=blob.content_type)


def etl_visits(visits):
    return [{
            'visitor': v.visitor,
            'timestamp': v.timestamp,
            'file_blob': v.file_gcs if hasattr(v, 'file_gcs') and v.file_gcs else v.file_blob
            } for v in visits]


@app.route('/', methods=['GET', 'POST'])
def root():
    'main application (GET/POST) handler'
    context = {}
    if request.method == 'GET':
        context['upload_url'] = url_for('upload')
    else:
        context['visits'] = etl_visits(fetch_visits(10))
    return render_template('index.html', **context)
