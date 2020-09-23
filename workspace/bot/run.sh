#! /bin/bash
while true; do python workspace/bot/tweet.py; sleep $(($RANDOM % 360 + 420)); done
