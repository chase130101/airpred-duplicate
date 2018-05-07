#!/bin/bash
#SBATCH -p general
#SBATCH -N 1 # number of nodes
#SBATCH -n 1 # number of cores
#SBATCH --mem 100000 # memory pool for all cores
#SBATCH -t 0-01:00 # time (D-HH:MM)
#SBATCH -o slurm.cnn2-pred-ensemble.%N.%j.out # STDOUT
#SBATCH -e slurm.cnn2-pred-ensemble.%N.%j.err # STDERR
python CNN2_pred_ensemble.py