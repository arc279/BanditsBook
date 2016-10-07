#!/bin/bash

#set -ue
export N_ARMS=25
export MEAN_TYPE=average
#export MEAN_TYPE=deflected
export BASE_DIR=~/workspace/R/annealing_softmax_results/${MEAN_TYPE}
export NUM_SIMS=5000
export HORIZON=250

[ ! -d $BASE_DIR ] && mkdir -p $BASE_DIR

cd ~/workspace/BanditsBook/

cd python
export BEST_ARM=$(python algorithms/softmax/test_annealing.py)
echo $BEST_ARM
cd -

(cd r/softmax && Rscript plot_annealing.R)
