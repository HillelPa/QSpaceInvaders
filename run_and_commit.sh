git pull
python3 run_game.py $1 $2 $3 0 --epsilon 0.2
git add *
git commit -m "auto e = 0.2"
git push
python3 run_game.py $1 $2 $3 0 --epsilon 0.4
git add *
git commit -m "auto avec epsilon = 0.4"
git push