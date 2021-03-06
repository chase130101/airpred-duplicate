#!/bin/bash
#SBATCH -p shared
#SBATCH -N 1 # number of nodes
#SBATCH -n 1 # number of cores
#SBATCH --mem 100000 # memory pool for all cores
#SBATCH -t 0-01:00 # time (D-HH:MM)
#SBATCH -o slurm.splitTVT.%N.%j.out # STDOUT
#SBATCH -e slurm.splitTVT.%N.%j.err # STDERR
python train_val_test_split.py --val --train_split 0.7 --val_split 0.1
