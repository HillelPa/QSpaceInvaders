git pull
python3 run_game.py $1 $2 $3 0 --epsilon 0.2
git add *
git commit -m "auto"
git push
python3 run_game.py $1 $2 $3 0
git add *
git commit -m "auto 2"
git push
