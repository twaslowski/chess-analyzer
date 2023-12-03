# Chess Analyzer

This is a self-learning project where I implemented my own chess game analysis using Stockfish. It runs as a Telegram bot – you can simply send it a PGN and it will perform an analysis based on the deviation of a player's actual move vs the ideal Stockfish move. The implementation is very naive and only manages to run at low depths in favour of speed. 

This project is not maintained anymore; the main point was to get analyses of chess.com games, but chess.com makes exporting PGNs on mobile unnecessarily hard, so I just use lichess, which offers unlimited analyses. It was primarily intended for learning anyhow.

## Usage

I'm hosting my instance of the chess analyzer on my own Raspberry Pi, which after a lot of benchmarking
I really cannot recommend. You can very easily host your own instance of this bot though – there
is a (very rudimentary) install script right now that is optimized for Raspberry Pis. In case you want
to do this on your own though, here's the most important steps:

Clone this repo: ```git clone git@github.com:TobiasWaslowski/chess-analyzer.git```

Optional: create a new Python virtual environment as to not clutter up your system:
```python3 -m venv venv ``` and ```source venv/bin/activate```.

Next up, install the necessary dependencies using pip: ```pip3 install -r requirements.txt```

You're also gonna want to install Stockfish and place the Stockfish binary somewhere Python can
access it (by default, that is chess-analyzer/Stockfish/bin/stockfish, but you can change that in
the config.json). For that, check out the [Stockfish Github Repo](https://github.com/official-stockfish/Stockfish)
where you can either download the binary or compile it yourself (which is what I did in order to optimize a bit).

After having done all that, just run the script with ```./run.sh```. This calls ```nohup```, which I
use because it's very convenient on a Raspberry. You could also call ```python3 src/main.py &``` and
be done with it – whatever works best for you. 

## Ideas

There are potential improvements that could be made to this bot. However, since lichess has its own unlimited analysis mode these days, it's pretty much obsolete. Still, if somebody would like to continue on this, here's some ideas.

- Calculation of an accuracy score
- Distinction into Blunders, Mistakes and Inaccuracies (based on eval difference?)
- Missed wins and faster mating lines
- A nice-looking infographic accumulating the scores throughout the game
- User settings regarding analysis depth/time, not having to see opponent mistakes
