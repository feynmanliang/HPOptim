# Author: Julien Hoachuck
# Copyright 2015, Julien Hoachuck, All rights reserved.
# findhp.sh: Allow easy modification invocation of  Spearmint to work with clusters etc.
duration=$2
dirPath=$1
mongod --fork --logpath $HOME/logs/mongod.log --dbpath $HOME/data/db
timeout $duration python $HOME/Spearmint/spearmint/main.py $dirPath
