# Step 1 - Migrate from `webapp2` to Flask

## Introduction

If you do not have a web UI, please skip to Step 2. The first step to moving to App Engine's next-generation (Gen2) runtimes is to move to a web framework that supports routing. This purpose of this codelab (and corresponding video) is to show ITDMs & developers what the migration steps are.

---

## Background

App Engine's first generation (Gen1) runtimes featured bundled services, and that is no longer the case for Gen2. The [`webapp` framework](https://web.archive.org/web/20170716061927/https://cloud.google.com/appengine/docs/standard/python/tools/webapp/) was bundled with Gen1 when App Engine first [launched on Python 2.5](http://googleappengine.blogspot.com/2008/04/introducing-google-app-engine-our-new.html) in 2008. Years later it was replaced by successor [`webapp2`](https://web.archive.org/web/20181027103713/https://cloud.google.com/appengine/docs/standard/python/tools/webapp2) when Gen1 [upgraded to Python 2.7](https://cloud.google.com/appengine/docs/standard/python/python25) in 2013.

While [`webapp2`](https://github.com/GoogleCloudPlatform/webapp2) (see [docs](https://webapp2.readthedocs.io/)) still exists and can be used outside of App Engine as a WSGI-compliant web framework, it doesn't have perform routing, and its core benefits are inextricably tied Gen1's bundled services, effectively deprecating it even though [it runs in Python 3 on Gen2](https://github.com/fili/webapp2-gae-python37) (also see [related issue](https://github.com/GoogleCloudPlatform/webapp2/issues/137)).

The purpose of this step is to show you a simple `webapp2` app and how you would migrate it to [Flask](https://flask.palletsprojects.com/), a popular micro web framework in the Python community that can be used on App Engine and many more services outside of Google Cloud, making apps more portable.

---

## Migration

The Python 2 App Engine runtime provides a set of "bundled" 3rd-party libraries where all you need to do is specify them in your `app.yaml` file to use. These "built-in" libraries are [listed here](https://cloud.google.com/appengine/docs/standard/python/tools/built-in-libraries-27). Unfortunately, 3rd-party libraries that are **not** must be installed locally in the `lib` folder in the application directory so everything is uploaded to the App Engine hosting service. This process is also known as "vendoring."

The Flask library is **not** built-in, and as such, users must list it (and other required/desired packages) in `requirements.txt`. Furthermore, the presence of *any* vendored libraries means App Engine needs to be told about the `lib` folder, and that's what the `appengine_config.py` configuration file is for. It should be placed in the same top-level application folder as `requirements.txt` and `lib`. Summarizing the steps to migrate web frameworks:

1. Create `requirements.txt` specifying Flask (versioning up to you)
1. Install package & dependencies with `pip install -t lib -r requirements.txt`.
1. Add an `appengine_config.py` to recognize external 3rd-party ("vendor") libraries
1. Flask requires HTML files to be placed in a `templates` folder, so create the folder and move `index.html` there, making a minor tweak moving from Django to Jinja2 templates.
1. Port web frameworks

These steps can also be found in the [documentation for copying 3rd-party libraries](https://cloud.google.com/appengine/docs/standard/python/tools/using-libraries-python-27#copying_a_third-party_library).

A key benefit of migrating to the latest Python 3 runtime: copying 3rd-party libraries is optional. You simply list them in `requirements.txt`; there's no `lib` folder nor `appengine_config.py` file.

### Configuration

When you're done with the first step, your `requirements.txt` file should look like this:

    Flask

After the next step, you should have a `lib` folder which looks like:

    bin/
    click/
    click-7.1.2.dist-info/
    flask/
    Flask-1.1.2.dist-info/
    itsdangerous/
    itsdangerous-1.1.0.dist-info/
    jinja2/
    Jinja2-2.11.2.dist-info/
    markupsafe/
    MarkupSafe-1.1.1.dist-info/
    werkzeug/
    Werkzeug-1.0.1.dist-info/

Create a file named `appengine_config.py` with the following contents:

```python
from google.appengine.ext import vendor

# Set PATH to your libraries folder.
PATH = 'lib'
# Add libraries installed in the PATH folder.
vendor.add(PATH)
```

Next, your `templates` folder will have just one file:

    index.html

One change is required in `index.html`: Add a pair of parentheses so `visit.timestamp.ctime` is updated to `visit.timestamp.ctime()`. Why? Django automatically executes Python callables whereas Jinja2 requires developers to explicitly use parentheses to affect the function/method call. (Ultimately this is more flexible because you can't call functions with parameters in Django.) This is the only change required (and `index.html` requires no additional changes for the remaining migration steps).

There is also a `.gcloudignore` that specifies config files that should not be deployed to App Engine. We're only porting web frameworks in this step. All other App Engine code stays the same. While this may make for a short tutorial, migrating web frameworks in a real application can be much more complex. If you start migrating the datastore here, chasing bugs down will be more challenging.

### Port from `webapp2` to Flask

#### At-a-glance

<table>
<tr>
<th>Description</th>
<th><code>webapp2</code></th>
<th>Flask</th>
</tr>
<tr>
<td>Startup</td>
<td>
<pre lang="python">
app = webapp2.WSGIApplication([
    ('/', MainHandler),
], debug=True)
</pre>
</td>
<td>
<pre lang="python">
app = Flask(__name__)
</pre>
</td>
</tr>
<tr>
<td>Handlers</td>
<td>
<pre lang="python">
class MainHandler(webapp2.RequestHandler):
    def get(self):
        store_visit(self.request.remote_addr, self.request.user_agent)
        visits = fetch_visits(10) or ()  # empty sequence if None
        tmpl = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(tmpl, {'visits': visits}))
</pre>
</td>
<td>
<pre lang="python">
@app.route('/')
def root():
    store_visit(request.remote_addr, request.user_agent)
    visits = fetch_visits(10) or ()  # empty sequence if None
    return render_template('index.html', visits=visits)
</pre>
</td>
</tr>
</table>

#### Imports

Let's start with the imports:

With `webapp2`, you import both the framework library as well as the App Engine extension to process Django-flavored templates:

```python
import webapp2
from google.appengine.ext.webapp import template
```

Flask uses Jinja2 templates instead. They're integrated so you can import that at the same time as Flask itself:

```python
from flask import Flask, render_template, request
```

#### Startup

`webapp2` apps are initialized with all the routes in a single array (Python list):

```python
app = webapp2.WSGIApplication([
    ('/', MainHandler),
], debug=True)
```

In Flask, you merely initialize the framework and use decorators to define the routes. As such, the call is much simpler:

```python
app = Flask(__name__)
```

#### Data model

Both versions use the App Engine NDB library to talk to the Datastore, so no change is required for Datastore access.

#### Handlers

This app has only one route (`/`) of execution: register this visit, and display the top 10 most recent "visits" via a pre-defined template file (`index.html`). `webapp2` uses a class-based execution model where handlers are written for supported HTTP methods. In our simple case, we only have `GET`:

```python
class MainHandler(webapp2.RequestHandler):
    def get(self):
        store_visit(self.request.remote_addr, self.request.user_agent)
        visits = fetch_visits(10) or ()  # empty sequence if None
        tmpl = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(tmpl, {'visits': visits}))
```

As mentioned above, Flask uses decorators for routing. It is also where supported HTTP methods are listed, such as `@app.route('/app/', methods=['GET', 'POST'])`. Since the default is only `GET` (and implicitly `HEAD`), it can be left off:

```python
@app.route('/')
def root():
    store_visit(request.remote_addr, request.user_agent)
    visits = fetch_visits(10) or ()  # empty sequence if None
    return render_template('index.html', visits=visits)
```

We know this isn't representative of your app or the effort, but it's to help you get started and focus on App Engine-specific updates.

#### Template HTML

Flask requires HTML files placed in a `templates` folder, so create the folder and move `index.html` there. Whereas `webapp2` templates execute callables without parentheses `( )`, Jinja2 requires the parentheses explicitly. While this sounds like a minor tweak, Jinja templates are more powerful because you can pass arguments in calls. Here's the 2-character update:

BEFORE:

```html+jinja
<li>{{ visit.timestamp.ctime }} from {{ visit.visitor }}</li>
```

AFTER:

```html+jinja
<li>{{ visit.timestamp.ctime() }} from {{ visit.visitor }}</li>
```

---

## Next

[**Step 2:**](/step2-flask-cloudndb-py2) The next tutorial involves migrating from App Engine NDB to Google Cloud NDB, a key step because after you switch to the Cloud library, many options become available to you.
