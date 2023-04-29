git pull
echo "Lancement 1 : e = 0.4"
python3 run_game.py $1 $2 $3 0 --epsilon 0.4
git add *
git commit -m "auto"
git push
echo "Lancement 2 : e = 0.1"
python3 run_game.py $1 $2 $3 0
git add *
git commit -m "auto 2"
git push
echo "Lancement 3 : e = 0.1"
python3 run_game.py $1 $2 $3 0
git add *
git commit -m "auto 3"
git push
echo "Lancement 4 : e = 0.1"
python3 run_game.py $1 $2 $3 0
git add *
git commit -m "auto 4"
git push
echo "Lancement 5 : e = 0.1"
python3 run_game.py $1 $2 $3 0
git add *
git commit -m "auto 5"
git push
echo "Lancement 6 : e = 0.1"
python3 run_game.py $1 $2 $3 0
git add *
git commit -m "auto 6"
git push