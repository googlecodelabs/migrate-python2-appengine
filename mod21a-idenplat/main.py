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

from flask import Flask, render_template, request
from google.auth import default
from google.cloud import ndb
from googleapiclient import discovery
from firebase_admin import auth, initialize_app

def _get_gae_admins():
    'return set of App Engine admins'
    # setup constants for calling Cloud IAM Resource Manager
    CREDS, PROJ_ID = default(  # Application Default Credentials and project ID
            ['https://www.googleapis.com/auth/cloud-platform'])
    IAM = discovery.build('cloudresourcemanager', 'v1', credentials=CREDS)
    _TARGETS = frozenset((     # App Engine admin roles
            'roles/viewer',
            'roles/editor',
            'roles/owner',
            'roles/appengine.appAdmin',
    ))

    # collate all users who are members of at least one GAE admin role (TARGETS)
    admins = set()             # set of all App Engine admins
    allow_policy = IAM.projects().getIamPolicy(resource=PROJ_ID).execute()
    for b in allow_policy['bindings']:  # bindings in IAM allow policy
        if b['role'] in _TARGETS:       # only look at GAE admin roles
            admins.update(user.split(':', 1)[1] for user in b['members'])
    return admins

@app.route('/is_admin', methods=['POST'])
def is_admin():
    'check if user (via their Firebase ID token) is GAE admin (POST) handler'
    id_token = request.headers.get('Authorization')
    email = auth.verify_id_token(id_token).get('email')
    return {'admin': email in _ADMINS}, 200


# initialize Flask, Firebase, Cloud NDB; fetch set of App Engine admins
app = Flask(__name__)
initialize_app()
ds_client = ndb.Client()
_ADMINS = _get_gae_admins()


class Visit(ndb.Model):
    'Visit entity registers visitor IP address & timestamp'
    visitor   = ndb.StringProperty()
    timestamp = ndb.DateTimeProperty(auto_now_add=True)

def store_visit(remote_addr, user_agent):
    'create new Visit entity in Datastore'
    with ds_client.context():
        Visit(visitor='{}: {}'.format(remote_addr, user_agent)).put()

def fetch_visits(limit):
    'get most recent visits'
    with ds_client.context():
        return Visit.query().order(-Visit.timestamp).fetch(limit)


@app.route('/')
def root():
    'main application (GET) handler'
    store_visit(request.remote_addr, request.user_agent)
    visits = fetch_visits(10)
    return render_template('index.html', visits=visits)
