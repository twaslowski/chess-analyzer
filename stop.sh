#!/bin/bash

if [ -f pid.txt ]; then
	pid=$(cat pid.txt)
	kill $pid
	echo "Stopped process $pid"
	rm pid.txt
else
	echo "The process most likely isn't running."
fi
