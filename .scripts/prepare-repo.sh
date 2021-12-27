#!/usr/bin/env bash

PACK_DIRECTORY=$(find . -maxdepth 1 -type d -not -path '*/\.*' -not -path '\.' | head -1 | sed -e 's/^\.\///')

if [[ -z "${PACK_DIRECTORY}" ]]; then
    echo "Unable to find pack directory"
    exit 1
fi

echo "Found pack directory: ${PACK_DIRECTORY}"

PACK_NAME=$(cat ${PACK_DIRECTORY}/pack.yaml | grep "name:" | sed -e 's/^name:[ \t]*//')

if [[ -z "${PACK_NAME}" ]]; then
    echo "Unable to retrieve pack name from ${PACK_DIRECTORY}/pack.yaml"
    exit 1
fi

echo "Found pack name: ${PACK_NAME}"


# Copy pack files in root dir so the checks work
echo "Exporting PACK_NAME and removing pack directory"

cp -r ${PACK_DIRECTORY}/* .
rm -rf ${PACK_DIRECTORY}

ls -la .

if [[ "${CIRCLECI}" == "true" ]]; then
    echo "export PACK_NAME=$PACK_NAME" >> ~/.circlerc
    echo "export FORCE_CHECK_ALL_FILES=true" >> ~/.circlerc
fi
