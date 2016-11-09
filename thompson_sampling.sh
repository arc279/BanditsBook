#!/bin/bash

#set -ue

export N_ARMS=250
#export MEAN_TYPE=average
export MEAN_TYPE=random
#export MEAN_TYPE=deflected
export BASE_DIR=~/workspace/R/ts_results
export NUM_SIMS=100
export HORIZON=10000

[ ! -d $BASE_DIR ] && mkdir -p $BASE_DIR

cd ~/workspace/BanditsBook/

cd python
export SAVE_FORMAT=$(python algorithms/thompson_sampling/test_ts.py)
cd - > /dev/null

echo $SAVE_FORMAT
(cd r/thompson_sampling && Rscript plot_ts.R)

