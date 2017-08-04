#!/bin/bash
#sample job submission scrip

# set the job name to hello
#SBATCH --job-name=pi

# send output to hello-world.out
#SBATCH --output=pi.out

# receive an email when job starts, ends, and fails
#SBATCH --mail-type=BEGIN,END,DAIL

# this job requests 1 core. Cores can be selected from various nodes.
#SBATCH --ntasks=1

# there are many partitions on Midway1 and it is important to specify which
# partition you want to run your job on. Not having the following option

# sandby partition on Midway1 will be selected as the default partition
#SBATCH --partition=sandyb

# Run the process 
./pi.cpp.exec
