#!/usr/bin/env bash

set -e

pip install virtualenv
virtualenv -p python3 .env
.env/bin/pip install -r requirements.txt