#!/bin/bash

set -ue

cd python

export NUM_SIMS=5000
export HORIZON=250
export N_ARMS=5
export BEST_ARM=$(python algorithms/hedge/test_hedge.py)

cd -

cd r/hedge && Rscript plot_hedge.R && cd -

