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
from google.appengine.api import users
from google.appengine.ext import ndb

app = Flask(__name__)


class Visit(ndb.Model):
    'Visit entity registers visitor IP address & timestamp'
    visitor   = ndb.StringProperty()
    timestamp = ndb.DateTimeProperty(auto_now_add=True)

def store_visit(remote_addr, user_agent):
    'create new Visit entity in Datastore'
    Visit(visitor='{}: {}'.format(remote_addr, user_agent)).put()

def fetch_visits(limit):
    'get most recent visits'
    return Visit.query().order(-Visit.timestamp).fetch(limit)


@app.route('/')
def root():
    'main application (GET) handler'
    store_visit(request.remote_addr, request.user_agent)
    visits = fetch_visits(10)

    # put together users context for web template
    user = users.get_current_user()
    context = {  # logged in
        'who':   user.nickname(),
        'admin': '(admin)' if users.is_current_user_admin() else '',
        'sign':  'Logout',
        'link':  '/_ah/logout?continue=%s://%s/' % (
                      request.environ['wsgi.url_scheme'],
                      request.environ['HTTP_HOST'],
                  ),  # alternative to users.create_logout_url()
    } if user else {  # not logged in
        'who':   'user',
        'admin': '',
        'sign':  'Login',
        'link':  users.create_login_url('/'),
    }

    # add visits to context and render template
    context['visits'] = visits  # display whether logged in or not
    return render_template('index.html', **context)
