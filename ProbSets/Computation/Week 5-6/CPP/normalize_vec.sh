#!/bin/bash

# send output to hello-world.out
#SBATCH --job-name=normalize_vec_openmp

# receive an email when job starts, ends, and fails
#SBATCH --output=normalize_vec_openmp.out

# this job requests 1 core. Cores can be selected from various nodes.
#SBATCH --ntasks=1

# there are many partitions on Midway1 and it is important to specify which
#SBATCH --cpus-per-task=8

# sandby partition on Midway1 will be selected as the default partition
#SBATCH --partition=sandyb

export OMP_NUM_THREADS=100

# Run the process
./normalize_vec.exec
