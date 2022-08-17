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
from google.appengine.api import taskqueue
from google.appengine.ext import ndb

HOUR = 3600
LIMIT = 10
TASKS = 1000
QUEUE = 'pullq'
app = Flask(__name__)


class Visit(ndb.Model):
    'Visit entity registers visitor IP address & timestamp'
    visitor   = ndb.StringProperty()
    timestamp = ndb.DateTimeProperty(auto_now_add=True)

def store_visit(remote_addr, user_agent):
    'create new Visit in Datastore and queue request to bump visitor count'
    Visit(visitor='{}: {}'.format(remote_addr, user_agent)).put()
    q = taskqueue.Queue(QUEUE)
    q.add(taskqueue.Task(payload=remote_addr, method='PULL'))

def fetch_visits(limit):
    'get most recent visits'
    return Visit.query().order(-Visit.timestamp).fetch(limit)


class VisitorCount(ndb.Model):
    visitor = ndb.StringProperty(repeated=False, required=True)
    counter = ndb.IntegerProperty()

def fetch_counts(limit):
    'get top visitors'
    return VisitorCount.query().order(-VisitorCount.counter).fetch(limit)


@app.route('/log')
def log_visitors():
    'worker processes recent visitor counts and updates them in Datastore'
    # tally recent visitor counts from queue then delete those tasks
    tallies = {}
    q = taskqueue.Queue(QUEUE)
    tasks = q.lease_tasks(HOUR, TASKS)
    for task in tasks:
        visitor = task.payload
        tallies[visitor] = tallies.get(visitor, 0) + 1
    if tasks:
        q.delete_tasks(tasks)

    # increment those counts in Datastore and return
    for visitor in tallies:
        counter = VisitorCount.query(VisitorCount.visitor == visitor).get()
        if not counter:
            counter = VisitorCount(visitor=visitor, counter=0)
            counter.put()
        counter.counter += tallies[visitor]
        counter.put()
    return 'DONE (with %d task[s] logging %d visitor[s])\r\n' % (
            len(tasks), len(tallies))


@app.route('/')
def root():
    'main application (GET) handler'
    store_visit(request.remote_addr, request.user_agent)
    context = {
        'limit':  LIMIT,
        'visits': fetch_visits(LIMIT),
        'counts': fetch_counts(LIMIT),
    }
    return render_template('index.html', **context)
