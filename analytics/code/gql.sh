#!/bin/bash

pip install ariadne
pip install dataclasses
pip install uvicorn

uvicorn analytics.code.api:app --host 0.0.0.0 --reload

