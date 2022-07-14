#!/bin/bash

DIRNAME="$(cd "$(dirname -- "$0")" >/dev/null; pwd -P)"
NAME="$(echo "${DIRNAME}" | rev | cut -d'/' -f1 | rev)"

echo "$NAME Installation !"
VENV_PATH='.venv'
echo "Creating Virtual Environment in: $VENV_PATH"

python3 -m venv "${VENV_PATH}"
source "${VENV_PATH}/bin/activate"
pip install update
pip install -r requirements.txt

echo 'To use the software do:'
echo "source '${VENV_PATH}/bin/activate'"
