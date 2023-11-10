#!/usr/bin/env bash
#
# Create virtualenv the datatrails_simplehashv1 command.
#
# 'task wheel' to generate installable wheel package generated locally.
#
rm -rf simplehash-venv/
python3 -m venv simplehash-venv
source simplehash-venv/bin/activate
python3 -m pip install -q --force-reinstall dist/datatrails_simplehash-*.whl
deactivate
