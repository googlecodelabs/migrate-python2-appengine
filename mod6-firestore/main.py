# Copyright 2021 Google LLC
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

from datetime import datetime
from flask import Flask, render_template, request
from google.cloud import firestore

app = Flask(__name__)
fs_client = firestore.Client()

def store_visit(remote_addr, user_agent):
    'create new Visit entity in Firestore'
    doc_ref = fs_client.collection('Visit')
    doc_ref.add({
        'timestamp': datetime.now(),
        'visitor': '{}: {}'.format(remote_addr, user_agent),
    })

def fetch_visits(limit):
    'get most recent visits'
    visits_ref = fs_client.collection('Visit')
    visits = (v.to_dict() for v in visits_ref.order_by('timestamp',
            direction=firestore.Query.DESCENDING).limit(limit).stream())
    return visits

@app.route('/')
def root():
    'main application (GET) handler'
    store_visit(request.remote_addr, request.user_agent)
    visits = fetch_visits(10)
    return render_template('index.html', visits=visits)
