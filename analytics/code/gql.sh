#!/bin/bash

pip install ariadne
pip install dataclasses

# pip install uvicorn
# uvicorn analytics.code.api:app --host 0.0.0.0 --reload

pip install flask
pip install flask_cors
python ./analytics/code/api.py 0.0.0.0 8000
