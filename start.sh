#!/bin/bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --chdir app
