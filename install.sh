#!/bin/bash

echo "Installing pip dependencies ..."
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

echo "Compiling stockfish ..."
git clone https://github.com/official-stockfish/Stockfish
cd stockfish/src
make build ARCH=armv7
