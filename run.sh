if [[ -z "${telegram_token_chess}" ]]; then
  echo "No token was found for deployment. Exiting."
  exit 1
else
	python3 src/main.py &
fi
