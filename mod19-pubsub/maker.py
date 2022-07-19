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

from __future__ import print_function
import google.auth
from google.api_core import exceptions
from google.cloud import pubsub

_, PROJECT_ID = google.auth.default()
TOPIC = 'pullq'
SBSCR = 'worker'
ppc_client = pubsub.PublisherClient()
psc_client = pubsub.SubscriberClient()
TOP_PATH = ppc_client.topic_path(PROJECT_ID, TOPIC)
SUB_PATH = psc_client.subscription_path(PROJECT_ID, SBSCR)

def make_top():
    try:
        top = ppc_client.create_topic(name=TOP_PATH)
        print('Created topic %r (%s)' % (TOPIC, top.name))
    except exceptions.AlreadyExists:
        print('Topic %r already exists at %r' % (TOPIC, TOP_PATH))

def make_sub():
    with psc_client:
        try:
            sub = psc_client.create_subscription(name=SUB_PATH, topic=TOP_PATH)
            print('Subscription created %r (%s)' % (SBSCR, sub.name))
        except exceptions.AlreadyExists:
            print('Subscription %r already exists at %r' % (SBSCR, SUB_PATH))

make_top()
make_sub()
