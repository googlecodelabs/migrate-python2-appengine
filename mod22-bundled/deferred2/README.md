# Module 22 - Using Deferred bundled service (Python 2)

This repo folder represents the Module 22 Python 2 sample app for the Deferred bundled service.

- The app implements a simple autoincrement counter which gets bumped for every page visit. The visit displays the current counter value then spawns a deferred task to bump it.
- The Python 2 version of the app uses the `webapp2` framework while the Python 3 version uses Flask and the App Engine SDK to access the bundled services.
- Also check out both `app.yaml` files for additional changes between runtimes.
- The Python 3 version of the app uses 3rd-party packages, and as such, has a `requirements.txt` file.
