#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

if [[ -d "${DIR}/venv" ]]
then
  source "${DIR}/venv/bin/activate"
else
  if ! python3 -m venv "${DIR}/venv"
  then
    echo "Error creating venv! Please fix!"
    exit 1
  else
    source "${DIR}/venv/bin/activate"
  fi
fi

python3 "./update_domain.py"