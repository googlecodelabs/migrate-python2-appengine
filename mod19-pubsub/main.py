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
import google.auth
from google.cloud import ndb, pubsub

LIMIT = 10
TASKS = 1000
TOPIC = 'pullq'
SBSCR = 'worker'

app = Flask(__name__)
ds_client  = ndb.Client()
ppc_client = pubsub.PublisherClient()
psc_client = pubsub.SubscriberClient()
_, PROJECT_ID = google.auth.default()
TOP_PATH = ppc_client.topic_path(PROJECT_ID, TOPIC)
SUB_PATH = psc_client.subscription_path(PROJECT_ID, SBSCR)


class Visit(ndb.Model):
    'Visit entity registers visitor IP address & timestamp'
    visitor   = ndb.StringProperty()
    timestamp = ndb.DateTimeProperty(auto_now_add=True)

def store_visit(remote_addr, user_agent):
    'create new Visit in Datastore and queue request to bump visitor count'
    with ds_client.context():
        Visit(visitor='{}: {}'.format(remote_addr, user_agent)).put()
    ppc_client.publish(TOP_PATH, remote_addr.encode('utf-8'))

def fetch_visits(limit):
    'get most recent visits'
    with ds_client.context():
        return Visit.query().order(-Visit.timestamp).fetch(limit)


class VisitorCount(ndb.Model):
    visitor = ndb.StringProperty(repeated=False, required=True)
    counter = ndb.IntegerProperty()

def fetch_counts(limit):
    'get top visitors'
    with ds_client.context():
        return VisitorCount.query().order(-VisitorCount.counter).fetch(limit)


@app.route('/log')
def log_visitors():
    'worker processes recent visitor counts and updates them in Datastore'
    # tally recent visitor counts from queue then delete those tasks
    tallies = {}
    acks = set()
    #with psc_client:
    rsp = psc_client.pull(subscription=SUB_PATH, max_messages=TASKS)
    msgs = rsp.received_messages
    for rcvd_msg in msgs:
        acks.add(rcvd_msg.ack_id)
        visitor = rcvd_msg.message.data.decode('utf-8')
        tallies[visitor] = tallies.get(visitor, 0) + 1
    if acks:
        psc_client.acknowledge(subscription=SUB_PATH, ack_ids=acks)
    if hasattr(psc_client, 'close'):
        try:
            psc_client.close()
        except AttributeError:
            pass

    # increment those counts in Datastore and return
    if tallies:
        with ds_client.context():
            for visitor in tallies:
                counter = VisitorCount.query(VisitorCount.visitor == visitor).get()
                if not counter:
                    counter = VisitorCount(visitor=visitor, counter=0)
                    counter.put()
                counter.counter += tallies[visitor]
                counter.put()
    return 'DONE (with %d task[s] logging %d visitor[s])\r\n' % (len(msgs), len(tallies))


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
