# Module 22 - Using Mail bundled service (Python 3)

This repo folder represents the Module 22 Python 3 sample app for the Mail bundled service.

- The app can receive email, saving only the most recent message received in Datastore. Visiting the app displays that message along with associated metadata (date, subject, sender).
- The Python 2 version of the app uses the `webapp2` framework while the Python 3 version uses Flask and the App Engine SDK to access the bundled services.
- Also check out both `app.yaml` files for additional changes between runtimes.
- The Python 3 version of the app uses 3rd-party packages, and as such, has a `requirements.txt` file.
