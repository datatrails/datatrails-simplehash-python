#!/usr/bin/env bash
#
# Manual testing of the datatrails_simplehashv1 command.
#
# 'task venv' to generate virtual environment
#
# Set environment variables with authtoken and client id/secret
#
source simplehash-venv/bin/activate

API_QUERY="https://app.dev-paul-0.wild.jitsuin.io"
API_QUERY+="/archivist/v2/assets/-/events"
API_QUERY+="?proof_mechanism=SIMPLE_HASH"
API_QUERY+="&timestamp_accepted_since=2022-10-07T07:01:34Z"
API_QUERY+="&timestamp_accepted_before=2022-10-16T13:14:56Z"
API_QUERY+="&order_by=SIMPLEHASHV1"

echo
echo Help
datatrails_simplehashv1 -h 

echo
echo "Get using token file"
if [ -n "${DATATRAILS_AUTHTOKEN_FILENAME}" ]
then
    datatrails_simplehashv1 \
        --auth-token-file "${DATATRAILS_AUTHTOKEN_FILENAME}" \
        "${API_QUERY}"
else
    echo "Cannot use authtoken - please set DATATRAILS_AUTHTOKEN_FILENAME"
fi

echo
echo "Get using client id and secret"
if [ -n "${DATATRAILS_APPREG_CLIENT}" -a "${DATATRAILS_APPREG_SECRET_FILENAME}" ]
then
    datatrails_simplehashv1 \
        --client-id "${DATATRAILS_APPREG_CLIENT}" \
        --client-secret-file "${DATATRAILS_APPREG_SECRET_FILENAME}" \
        "${API_QUERY}"
else
    echo "Cannot use appregistration - please set DATATRAILS_APPREG_CLIENT"
    echo "Cannot use appregistration - please set DATATRAILS_APPREG_SECRET_FILENAME"
fi

API_QUERY="https://app.datatrails.ai"
API_QUERY+="/archivist/v2/publicassets/-/events"
API_QUERY+="?proof_mechanism=SIMPLE_HASH"
API_QUERY+="&timestamp_accepted_since=2022-10-07T07:01:34Z"
API_QUERY+="&timestamp_accepted_before=2022-10-16T13:14:56Z"
API_QUERY+="&order_by=SIMPLEHASHV1"

echo
echo "Get public assets"
datatrails_simplehashv1 "${API_QUERY}"

deactivate
