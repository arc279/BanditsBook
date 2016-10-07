#!/bin/bash

#set -ue
export N_ARMS=25
export MEAN_TYPE=average
export BASE_DIR=~/workspace/R/exp3_results/${MEAN_TYPE}
export NUM_SIMS=5000
export HORIZON=2500

[ ! -d $BASE_DIR ] && mkdir -p $BASE_DIR

cd ~/workspace/BanditsBook/

cd python
export BEST_ARM=$(python algorithms/exp3/test_exp3.py)
echo $BEST_ARM
cd -

(cd r/exp3 && Rscript plot_exp3.R)

