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
import json
import logging
import time
from flask import Flask, render_template, request
import google.auth
from google.cloud import ndb, tasks

app = Flask(__name__)
ds_client = ndb.Client()
ts_client = tasks.CloudTasksClient()

_, PROJECT_ID = google.auth.default()
REGION_ID = 'REGION_ID'    # replace w/your own
QUEUE_NAME = 'default'     # replace w/your own
QUEUE_PATH = ts_client.queue_path(PROJECT_ID, REGION_ID, QUEUE_NAME)

class Visit(ndb.Model):
    'Visit entity registers visitor IP address & timestamp'
    visitor   = ndb.StringProperty()
    timestamp = ndb.DateTimeProperty(auto_now_add=True)

def store_visit(remote_addr, user_agent):
    'create new Visit entity in Datastore'
    with ds_client.context():
        Visit(visitor='{}: {}'.format(remote_addr, user_agent)).put()

def fetch_visits(limit):
    'get most recent visits & add task to delete older visits'
    with ds_client.context():
        data = Visit.query().order(-Visit.timestamp).fetch(limit)
    oldest = time.mktime(data[-1].timestamp.timetuple())
    oldest_str = time.ctime(oldest)
    logging.info('Delete entities older than %s' % oldest_str)
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
    return (v.to_dict() for v in data), oldest_str

@app.route('/trim', methods=['POST'])
def trim():
    '(push) task queue handler to delete oldest visits'
    oldest = float(request.get_json().get('oldest'))
    with ds_client.context():
        keys = Visit.query(
                Visit.timestamp < datetime.fromtimestamp(oldest)
        ).fetch(keys_only=True)
        nkeys = len(keys)
        if nkeys:
            logging.info('Deleting %d entities: %s' % (
                    nkeys, ', '.join(str(k.id()) for k in keys)))
            ndb.delete_multi(keys)
        else:
            logging.info(
                    'No entities older than: %s' % time.ctime(oldest))
    return ''   # need to return SOME string w/200

@app.route('/')
def root():
    'main application (GET) handler'
    store_visit(request.remote_addr, request.user_agent)
    visits, oldest = fetch_visits(10)
    context = {'visits': visits, 'oldest': oldest}
    return render_template('index.html', **context)
