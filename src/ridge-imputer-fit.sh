#!/bin/bash
#SBATCH -p shared
#SBATCH -N 1 # number of nodes
#SBATCH -n 1 # number of cores
#SBATCH --mem 100000 # memory pool for all cores
#SBATCH -t 0-05:00 # time (D-HH:MM)
#SBATCH -o slurm.ridgeImputerFit.%N.%j.out # STDOUT
#SBATCH -e slurm.ridgeImputerFit.%N.%j.err # STDERR
python ridge_imputer_fit.py --val --impute_split 0.3 --max_iter 10 --initial_strategy mean --alpha 0.0001 
