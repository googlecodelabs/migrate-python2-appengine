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

from cgi import escape
import webapp2
from google.appengine.ext import ndb
from google.appengine.ext.webapp import mail_handlers

KEY_NAME = 'SECRET'
FIELDS = frozenset(('sender', 'subject', 'date'))
MSG_TMPL = '''\
<h2>Last message received:</h2><p></p>
<pre>
From: %(sender)s
Subject: %(subject)s
Date: %(date)s

%(body)s
</pre>
'''

class LastMsg(ndb.Model):
    'LastMsg entity for registering last-received email message'
    sender  = ndb.StringProperty(indexed=False)
    subject = ndb.StringProperty(indexed=False)
    date    = ndb.StringProperty(indexed=False)
    body    = ndb.StringProperty(indexed=False)


class EmailHandler(mail_handlers.InboundMailHandler):
    '''
    email receipt (POST) handler:
        - extract email message from request payload
        - get last message singleton entity (or create empty one)
        - add core values: sender, subject, date
        - extract and decode text (from first plain text body)
        - save entity and return
    '''
    def receive(self, msg):
        last_msg = LastMsg.get_or_insert(KEY_NAME, sender='')
        # quick loop to assign last_msg.FIELD = msg.FIELD for each field
        for field in FIELDS:
            setattr(last_msg, field, getattr(msg, field))
        last_msg.body = (msg.bodies('text/plain').next())[1].decode()
        last_msg.put()


class MainHandler(webapp2.RequestHandler):
    '''
    main application (GET) handler:
        - get last-message entity from Datastore
        - convert to dict then escape special characters
        - drop values into template and return
    '''
    def get(self):
        last_msg = LastMsg.get_by_id(KEY_NAME)
        msg_dict = last_msg.to_dict()
        self.response.write(
                MSG_TMPL % dict((k, escape(msg_dict[k])) for k in msg_dict))


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/_ah/mail/.+', EmailHandler),
], debug=True)
