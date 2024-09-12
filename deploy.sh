echo "ANURAG DEPLOYING APP"
echo "SETTING VIRTUAL ENVIRONMENT"
python3 -m venv AppVenv
source AppVenv/bin/activate

echo "CHECKING IF APP RUNNING"
ps -ef | grep main

echo "KILLING EXISTING APP"
pkill -f main

echo "CHECKING IF APP RUNNING"
ps -ef | grep main

dir_name=$(date +"%Y-%m-%d-%H-%M-%S")
mkdir "$dir_name"
cp /path/to/file "$dir_name"/

mkdir $(date +"%Y%m%d_%H%M%S")
echo "COLLECTING LOGS"
cp -r LOGS/ "$dir_name"/
cp -r CONSOLE_OUTPUT.txt "$dir_name"/

echo "STARTING NEW APP"
nohup python main.py > CONSOLE_OUTPUT.txt &

echo "CHECKING IF APP RUNNING"
ps -ef | grep main

echo "ALL DONE"
