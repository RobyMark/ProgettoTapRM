#!/bin/bash
[[ -z "${PYTHON_APP}" ]] && { echo "PYTHON_APP required"; exit 1; }
PYTHON_DIR="/usr/src/app/"

echo "Running python ${PYTHON_APP} (Python Dir:${PYTHON_DIR})"
cd /usr/src/app/
if [ "${PYTHON_APP}" = "GetSteamReviews.py" ]
then
    echo "HIIII!!!!!"
    python ${PYTHON_APP} $1 $2
else
    python ${PYTHON_APP}
fi