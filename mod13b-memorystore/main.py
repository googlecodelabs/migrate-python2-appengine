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

import os
import pickle
from flask import Flask, render_template, request
from google.cloud import ndb
import redis

app = Flask(__name__)
ds_client = ndb.Client()
HOUR = 3600
REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
REDIS_PORT = os.environ.get('REDIS_PORT', '6379')
REDIS = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)

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
    # check for (hour-)cached visits
    ip_addr, usr_agt = request.remote_addr, request.user_agent
    visitor = '{}: {}'.format(ip_addr, usr_agt)
    rsp = REDIS.get('visits')
    visits = pickle.loads(rsp) if rsp else None

    # register visit & run DB query if cache empty or new visitor
    if not visits or visits[0].visitor != visitor:
        store_visit(ip_addr, usr_agt)
        visits = list(fetch_visits(10))
        REDIS.set('visits', pickle.dumps(visits), ex=HOUR)

    return render_template('index.html', visits=visits)
