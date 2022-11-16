#!/usr/bin/env bash
#
# Manual testing of the rkvst_simplehashv1 command.
#
# 'task wheel' to generate installable wheel package generated locally.
#
# Populate the credentials directory with client id and secret and
# change the fqdn field.
# The credentials  must be for a particular tenant identity.
# Vary start and end time and execute such that:
#
#    1. illegal url - check correct response
#    2. bad token - check correct response
#    3. vary start and endtimes and check that a simplehash is calculated.
#
python3 -m venv simplehash-venv
source simplehash-venv/bin/activate
python3 -m pip install -q --force-reinstall dist/rkvst_simplehash-*.whl

CLIENT_ID=$(cat credentials/client_id)
rkvst_simplehashv1 \
    --client-id "${CLIENT_ID}" \
    --client-secret-file "credentials/client_secret" \
    --fqdn "app.rkvst-test.io" \
    --start-time "2022-11-16T15:59:14Z" \
    --end-time "2022-11-16T15:59:22Z"

deactivate
rm -rf simplehash-venv

