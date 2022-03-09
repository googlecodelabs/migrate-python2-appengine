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
from webapp2_extras import jinja2
from google.appengine.api import app_identity
from google.appengine.ext import blobstore, ndb
from google.appengine.ext.webapp import blobstore_handlers

BUCKET = app_identity.get_default_gcs_bucket_name()


class BaseHandler(webapp2.RequestHandler):
    'Derived request handler mixing-in Jinja2 support'
    @webapp2.cached_property
    def jinja2(self):
        return jinja2.get_jinja2(app=self.app)

    def render_response(self, _template, **context):
        self.response.write(self.jinja2.render_template(_template, **context))


class Visit(ndb.Model):
    'Visit entity registers visitor IP address & timestamp'
    visitor   = ndb.StringProperty()
    timestamp = ndb.DateTimeProperty(auto_now_add=True)
    file_blob = ndb.BlobKeyProperty()


def store_visit(remote_addr, user_agent, upload_key):
    'create new Visit entity in Datastore'
    Visit(visitor='{}: {}'.format(remote_addr, user_agent),
            file_blob=upload_key).put()


def fetch_visits(limit):
    'get most recent visits'
    return Visit.query().order(-Visit.timestamp).fetch(limit)


class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    'Upload blob (POST) handler'
    def post(self):
        uploads = self.get_uploads()
        blob_id = uploads[0].key() if uploads else None
        store_visit(self.request.remote_addr, self.request.user_agent, blob_id)
        self.redirect('/', code=307)


class ViewBlobHandler(blobstore_handlers.BlobstoreDownloadHandler):
    'view uploaded blob (GET) handler'
    def get(self, blob_key):
        self.send_blob(blob_key) if blobstore.get(blob_key) else self.error(404)


class MainHandler(BaseHandler):
    'main application (GET/POST) handler'
    def get(self):
        self.render_response('index.html',
                upload_url=blobstore.create_upload_url('/upload',
                gs_bucket_name=BUCKET))

    def post(self):
        visits = fetch_visits(10)
        self.render_response('index.html', visits=visits)


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/upload', UploadHandler),
    ('/view/([^/]+)?', ViewBlobHandler),
], debug=True)
