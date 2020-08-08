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

import os
import webapp2
from google.appengine.ext import ndb
from google.appengine.ext.webapp import template

class Visit(ndb.Model):
    visitor   = ndb.StringProperty()
    timestamp = ndb.DateTimeProperty(auto_now_add=True)

def store_visit(remote_addr, user_agent):
    Visit(visitor='{}: {}'.format(remote_addr, user_agent)).put()

def fetch_visits(limit):
    return (v.to_dict() for v in Visit.query().order(
        -Visit.timestamp).fetch_page(limit)[0])

class MainHandler(webapp2.RequestHandler):
    def get(self):
        store_visit(self.request.remote_addr, self.request.user_agent)
        visits = fetch_visits(10) or ()  # empty sequence if None
        tmpl = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(tmpl, {'visits': visits}))

app = webapp2.WSGIApplication([
    ('/', MainHandler),
], debug=True)
