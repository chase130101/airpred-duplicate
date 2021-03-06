#!/bin/bash
#SBATCH -p shared
#SBATCH -N 1 # number of nodes
#SBATCH -n 1 # number of cores
#SBATCH --mem 100000 # memory pool for all cores
#SBATCH -t 0-01:00 # time (D-HH:MM)
#SBATCH -o slurm.dataSetup.%N.%j.out # STDOUT
#SBATCH -e slurm.dataSetup.%N.%j.err # STDERR
Rscript data_setup.R
