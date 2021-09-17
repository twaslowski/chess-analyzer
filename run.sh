if [[ -z "${telegram_token_chess}" ]]; then
  echo "No token was found for deployment. Exiting."
  exit 1
else
  docker build -t chess-analyzer .
  docker run --env telegram_token_chess=${telegram_token_chess} chess-analyzer
fi
