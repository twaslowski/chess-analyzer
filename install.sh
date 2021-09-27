#!/bin/bash

echo "Installing pip dependencies ..."
pip install -r requirements.txt

echo "Compiling stockfish ..."
git clone https://github.com/official-stockfish/Stockfish
cd stockfish/src
make build ARCH=armv7
