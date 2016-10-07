#!/bin/bash

#set -ue
export N_ARMS=25
#export MEAN_TYPE=average
export MEAN_TYPE=random
#export MEAN_TYPE=deflected
export BASE_DIR=~/workspace/R/ts2_results/${MEAN_TYPE}
export NUM_SIMS=1000
export HORIZON=5000

[ ! -d $BASE_DIR ] && mkdir -p $BASE_DIR

cd ~/workspace/BanditsBook/

cd python
python algorithms/thompson_sampling/test_ts2.py
cd -

(cd r/thompson_sampling && Rscript plot_ts2.R)

