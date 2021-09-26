#!/bin/bash

if [[ -z "${telegram_token_chess}" ]]; then
  echo "No token was found for deployment. Exiting."
  exit 1
else
	nohup src/main.py &
	echo $! > pid.txt
fi
