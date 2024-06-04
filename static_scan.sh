#!/bin/bash

# Created a script to activate venv and run Static Code Analysis,
# Saved in an "static.output" file.

source venv/bin/activate
 
flake8 . | tee static.output
exit 0

