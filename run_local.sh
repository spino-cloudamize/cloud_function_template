#!/usr/bin/env bash

source local.env
export FLASK_APP=local_run.py
flask run --debugger