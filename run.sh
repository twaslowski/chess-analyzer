#!/bin/bash

if [[ -z "${telegram_token_chess}" ]]; then
  echo "No token was found for deployment. Exiting."
  exit 1
else
  source venv/bin/activate
	nohup code/src/main.py &
	echo $! > pid.txt
fi
