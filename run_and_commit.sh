git pull
python3 run_game.py $1 $2 $3 0.3 False
git add *
git commit -m "auto"
git push
python3 run_game.py $1 $2 $3 0.1 False
git add *
git commit -m "auto"
git push
