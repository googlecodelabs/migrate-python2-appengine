# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from datetime import datetime
import os
from flask import Flask, render_template, request
from google.cloud import datastore

app = Flask(__name__)
ds_client = datastore.Client()

def store_visit(remote_addr, user_agent):
    entity = datastore.Entity(key=ds_client.key('Visit'))
    entity.update({
        'timestamp': datetime.now(),
        'visitor': '{}: {}'.format(remote_addr, user_agent),
    })
    ds_client.put(entity)

def fetch_visits(limit):
    query = ds_client.query(kind='Visit')
    query.order = ['-timestamp']
    return query.fetch(limit=limit)

@app.route('/')
def root():
    store_visit(request.remote_addr, request.user_agent)
    visits = fetch_visits(10) or ()  # empty sequence if None
    return render_template('index.html', visits=visits)

if __name__ == '__main__':
    app.run(debug=True, threaded=True, host='0.0.0.0',
            port=int(os.environ.get('PORT', 8080)))
