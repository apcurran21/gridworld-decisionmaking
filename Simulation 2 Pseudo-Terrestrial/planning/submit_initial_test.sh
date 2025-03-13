#!/bin/bash
#SBATCH -A e32704
#SBATCH -p normal
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=2
#SBATCH --mem-per-cpu=16G
#SBATCH -t 15:00:00
#SBATCH --job-name="single_sim_test"
#SBATCH --mail-type=ALL
#SBATCH --mail-user=andycurran2025@u.northwestern.edu
#SBATH --constraint="[quest7|quest8|quest9|quest10]"

# it seems like I can just use my normal version of python w/ `research` env
module purge
eval "$(conda shell.bash hook)"
conda activate /home/apc6353/.conda/envs/research

# path to the python script
script_path="/projects/e32704/andy/decisionmaking/gridworld-decisionmaking/Simulation 2 Pseudo-Terrestrial/planning/new_main.py"

mpiexec -n ${SLURM_NTASKS} python "$script_path"
