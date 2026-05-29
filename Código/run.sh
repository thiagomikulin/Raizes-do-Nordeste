#!/bin/bash
if [ -z "$VIRTUAL_ENV" ]; then
    source ./venv/bin/activate
fi

uvicorn main:app --reload