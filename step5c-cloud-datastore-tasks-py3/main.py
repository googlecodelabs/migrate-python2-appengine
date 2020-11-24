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

import json
from datetime import datetime
import time
from flask import Flask, render_template, request
from google.cloud import datastore, tasks

app = Flask(__name__)
ds_client = datastore.Client()
ts_client = tasks.CloudTasksClient()

PROJECT_ID = 'PROJECT_ID'
REGION_ID = 'REGION_ID'
QUEUE_NAME = 'default'
QUEUE_PATH = ts_client.queue_path(PROJECT_ID, REGION_ID, QUEUE_NAME)

def store_visit(remote_addr, user_agent):
    'create new Visit entity in Datastore'
    entity = datastore.Entity(key=ds_client.key('Visit'))
    entity.update({
        'timestamp': datetime.now(),
        'visitor': '{}: {}'.format(remote_addr, user_agent),
    })
    ds_client.put(entity)

def fetch_visits(limit):
    'get most recent visits & add task to delete older visits'
    query = ds_client.query(kind='Visit')
    query.order = ['-timestamp']
    data = list(query.fetch(limit=limit))
    oldest = time.mktime(data[-1]['timestamp'].timetuple())
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
    ts_client.create_task(parent=QUEUE_PATH, task=task)
    return data, oldest_str

@app.route('/trim', methods=['POST'])
def trim():
    '(push) task queue handler to delete oldest visits'
    oldest = float(request.get_json().get('oldest'))
    query = ds_client.query(kind='Visit')
    query.add_filter('timestamp', '<', datetime.fromtimestamp(oldest))
    query.keys_only()
    keys = list(query.fetch())
    nkeys = len(keys)
    if nkeys:
        print('Deleting %d entities: %s' % (
                nkeys, ', '.join(str(k.id) for k in keys)))
        ds_client.delete_multi(keys)
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
