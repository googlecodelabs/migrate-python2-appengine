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

from flask import Flask
from google.appengine.api import wrap_wsgi_app
from google.appengine.ext import deferred, ndb

KEY_NAME = 'SECRET'
OUTPUT = '''\
<title>Module 22 Deferred sample app</title>
Counter at %d... bump requested.
'''
app = Flask(__name__)
app.wsgi_app = wrap_wsgi_app(app.wsgi_app, use_deferred=True)

class Counter(ndb.Model):
    'Counter entity: autoincrement integer'
    count = ndb.IntegerProperty(indexed=False)


def bump_counter_later(key):
    'bump counter in (push) task'
    entity = Counter.get_or_insert(key, count=0)
    entity.count += 1
    entity.put()


@app.route('/')
def root():
    'main application (GET) handler'
    entity = Counter.get_by_id(KEY_NAME)
    output = OUTPUT % (entity.count if entity else 0)
    deferred.defer(bump_counter_later, KEY_NAME)
    return output
