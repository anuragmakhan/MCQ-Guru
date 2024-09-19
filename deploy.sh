#!/bin/bash

echo "ANURAG DEPLOYING APP"
echo "SETTING VIRTUAL ENVIRONMENT"
python3 -m venv AppVenv
source AppVenv/bin/activate

pip install -r requirements.txt

echo "CHECKING IF APP RUNNING"
ps -ef | grep main

echo "KILLING EXISTING APP"
pkill -f main

echo "CHECKING IF APP RUNNING"
ps -ef | grep main

mkdir $(date +"%Y%m%d_%H%M%S")
echo "COLLECTING LOGS"
cp -r LOG/ "$dir_name"/
cp -r CONSOLE_OUTPUT.txt "$dir_name"/

echo "PULLING LATEST CODE"
git checkout .
git pull

echo "STARTING NEW APP"
nohup python main.py > CONSOLE_OUTPUT.txt &

echo "CHECKING IF APP RUNNING"
ps -ef | grep main

echo "ALL DONE"
