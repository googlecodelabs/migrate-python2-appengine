# Step 4 (EXTRA) - Migrate from Google App Engine to Cloud Run and port to Python 3 (with Docker)

## Introduction

After migrating to Cloud Run, the only changes that need to be made to port the application to Python 3 is to remove the Unicode string identifiers, and even this is optional as they're ignored by 3.x interpreters.

---

## Migration

Porting from Python 2 to 3 is not within the scope of this tutorial, and our simple sample app is already 2-3 compatible, so the only changes required are in configuration.

1. Designate using Python 3 in your `Dockerfile` if you have one. Buildpacks auto-detect this.
1. Any `.dockerignore` should remain as-is.
1. Optionally remove the Unicode string literal designations in `main.py` (see the `diff`s below)

### Configuration

The only real change for this app is to switch the `Dockerfile FROM` directive from `FROM python:2-slim` to `FROM python:3-slim`.

---

## Next

Congratulations... this app is fully modernized now, concluding this tutorial.
