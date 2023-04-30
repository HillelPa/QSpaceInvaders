git pull
python3 run_game.py $1 $2 $3 0 
git add *
git commit -m "auto"
git push
python3 run_game.py $1 $2 $3 0
git add *
git commit -m "auto 1"
git push
python3 run_game.py $1 $2 $3 0
git add *
git commit -m "auto 2"
git push
python3 run_game.py $1 $2 $3 0
git add *
git commit -m "auto 3"
git push
python3 run_game.py $1 $2 $3 0
git add *
git commit -m "auto 4"
git push
python3 run_game.py $1 $2 $3 0
git add *
git commit -m "auto 5"
git push
python3 run_game.py $1 $2 $3 0 --epsilon 0
git add *
git commit -m "auto avec epsilon = 0"
git push