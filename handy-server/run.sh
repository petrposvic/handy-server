#!/bin/bash

print_usage() {
  echo "Usage:"
  echo "  $0 [fg|bg]"
}

if [ $# -ne 1 ]; then
  print_usage
  exit 1
fi

SCRIPT_DIR="$(dirname $(readlink -f $0))"
cd $SCRIPT_DIR

if [ "$1" == "bg" ]; then
  screen -S stream-launcher -d -m ./run.sh fg
  echo "Resume detached screen:"
  echo "  screen -r stream-launcher"
elif [ "$1" == "fg" ]; then
  . ../handy-server-venv/bin/activate
  uwsgi --socket 0.0.0.0:5000 --protocol=http -w wsgi:app
  deactivate
else
  print_usage
fi

