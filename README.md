# Chess Analyzer

This is a Telegram bot that analyzes your chess games for you. Simply send it a PGN with your game
(via the "Share" feature in lichess or "Download" in chess.com) and you will get an analysis. 
Right now, the logic for the analysis is very primitive, but I'm working on improving it.

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

## Contributing

Of course I'd be very happy if you decided to contribute to this repository! Just open a pull request :)

## Backlog

There are some ideas I'm trying to implement right now. Here's a list, in no particular order. If you're interested
in implementing one of those features, hit me up:

- Calculation of an accuracy score
- Distinction into Blunders, Mistakes and Inaccuracies
- Missed wins and faster mating lines
- A nice-looking infographic accumulating the scores throughout the game
- User settings regarding analysis depth/time, not having to see opponent mistakes and other good stuff

## Reporting Issues

If there's anything wrong with the code, feel free to open an issue. Please describe your issue with as
much detail as you can so I can get on fixing it as easily as possible.