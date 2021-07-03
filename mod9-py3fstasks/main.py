# Copyright 2020 Google LLC
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
import json
import time
from flask import Flask, render_template, request
import google.auth
from google.cloud import firestore, tasks

app = Flask(__name__)
fs_client = firestore.Client()
ts_client = tasks.CloudTasksClient()

_, PROJECT_ID = google.auth.default()
REGION_ID = 'REGION_ID'    # replace w/your own
QUEUE_NAME = 'default'     # replace w/your own
QUEUE_PATH = ts_client.queue_path(PROJECT_ID, REGION_ID, QUEUE_NAME)
PATH_PREFIX = QUEUE_PATH.rsplit('/', 2)[0]

def store_visit(remote_addr, user_agent):
    'create new Visit document in Firestore'
    doc_ref = fs_client.collection('Visit')
    doc_ref.add({
        'timestamp': datetime.now(),
        'visitor': '{}: {}'.format(remote_addr, user_agent),
    })

def _create_queue_if():
    'app-internal function creating default queue if it does not exist'
    try:
        ts_client.get_queue(name=QUEUE_PATH)
    except Exception as e:
        if 'does not exist' in str(e):
            ts_client.create_queue(parent=PATH_PREFIX,
                    queue={'name': QUEUE_PATH})
    return True

def fetch_visits(limit):
    'get most recent visits & add task to delete older visits'
    visits_ref = fs_client.collection('Visit')
    visits = list(v.to_dict() for v in visits_ref.order_by('timestamp',
            direction=firestore.Query.DESCENDING).limit(limit).stream())
    oldest = time.mktime(visits[-1]['timestamp'].timetuple())
    oldest_str = time.ctime(oldest)
    print('Delete entities older than %s' % oldest_str)
    task = {
        'app_engine_http_request': {
            'relative_uri': '/trim',
            'body': json.dumps({'oldest': oldest}).encode(),
            'headers': {
                'Content-Type': 'application/json',
            },
        }
    }
    if _create_queue_if():
        ts_client.create_task(parent=QUEUE_PATH, task=task)
    return visits, oldest_str

def _delete_docs(visits):
    'app-internal generator deleteing all old FS visit documents'
    for visit in visits:
        visit.reference.delete()
        yield visit.id

@app.route('/trim', methods=['POST'])
def trim():
    '(push) task queue handler to delete oldest visits'
    oldest = float(request.get_json().get('oldest'))
    query = fs_client.collection('Visit')
    visits = query.where('timestamp', '<',
            datetime.fromtimestamp(oldest)).stream()
    dlist = ', '.join(str(v_id) for v_id in _delete_docs(visits))
    if dlist:
        print('Deleting %d entities: %s' % (dlist.count(',')+1, dlist))
    else:
        print('No entities older than: %s' % time.ctime(oldest))
    return ''   # need to return SOME string w/200

@app.route('/')
def root():
    'main application (GET) handler'
    store_visit(request.remote_addr, request.user_agent)
    visits, oldest = fetch_visits(10)
    context = {'visits': visits, 'oldest': oldest}
    return render_template('index.html', **context)
