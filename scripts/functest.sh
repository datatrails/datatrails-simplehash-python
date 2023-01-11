#!/usr/bin/env bash
#
# Manual testing of the rkvst_simplehashv1 command.
#
# 'task venv' to generate virtual environment
#
# Populate the credentials directory with auth token and change the fqdn field.
# The auth token must be for a particular tenant identity.
# Vary start and end time and execute such that:
# 
#    1. illegal url - check correct response
#    2. bad token - check correct response
#    3. vary start and endtimes and check that a simplehash is calculated.
#
source simplehash-venv/bin/activate

rkvst_simplehashv1 \
    --auth-token-file "credentials/token" \
    --fqdn "app.dev-paul-0.wild.jitsuin.io" \
    --start-time "2022-11-24T15:57:26Z" \
    --end-time "2022-11-24T15:57:30Z"


deactivate
