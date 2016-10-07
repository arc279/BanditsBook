#!/bin/bash

#set -ue
export N_ARMS=25
export MEAN_TYPE=average
#export MEAN_TYPE=deflected
#export MEAN_TYPE=random
export BASE_DIR=~/workspace/R/magi_results/${MEAN_TYPE}
export NUM_SIMS=5000
export HORIZON=2500

[ ! -d $BASE_DIR ] && mkdir -p $BASE_DIR

cd ~/workspace/BanditsBook/

cd python
export BEST_ARM=$(python algorithms/magi.py)
echo $BEST_ARM
cd -

(cd r && Rscript plot_magi.R)
