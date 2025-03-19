#!/bin/bash
#SBATCH -A e32704
#SBATCH -p normal
#SBATCH --nodes=8
#SBATCH --ntasks-per-node=16
#SBATCH --mem-per-cpu=3256M
#SBATCH -t 24:00:00
#SBATCH --job-name="initial_sim_test"
#SBATCH --mail-type=ALL
#SBATCH --mail-user=andycurran2025@u.northwestern.edu
## #SBATCH --constraint="[quest7|quest8|quest9|quest10]" ## I think this is outdated
#SBATCH --constraint="[quest8|quest9|quest10|quest11]"


# it seems like I can just use my normal version of python w/ `research` env
module purge
eval "$(conda shell.bash hook)"
conda activate /home/apc6353/.conda/envs/decision-making-py310

# path to the python script
script_path="/projects/e32704/andy/decisionmaking/gridworld-decisionmaking/Simulation 2 Pseudo-Terrestrial/planning/new_main.py"

mpiexec -n ${SLURM_NTASKS} python "$script_path"
