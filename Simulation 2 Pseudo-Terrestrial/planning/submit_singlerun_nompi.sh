#!/bin/bash
#SBATCH -A e32704
###SBATCH -p normal
#SBATCH -p short
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
###SBATCH -t 15:00:00
#SBATCH -t 01:00:00
#SBATCH --job-name="single_nompi_test"
#SBATCH --mail-type=ALL
#SBATCH --mail-user=andycurran2025@u.northwestern.edu
#SBATCH --output=s_out-%j.out
#SBATCH --error=s_err-%j.err


# it seems like I can just use my normal version of python w/ `research` env
module purge
eval "$(conda shell.bash hook)"
conda activate /home/apc6353/.conda/envs/decision-making-py310

# path to the python script
# script_path="/projects/e32704/andy/decisionmaking/gridworld-decisionmaking/Simulation 2 Pseudo-Terrestrial/planning/new_main.py"
script_path="/projects/e32704/andy/decisionmaking/gridworld-decisionmaking/Simulation 2 Pseudo-Terrestrial/planning/main_singlerun_nompi.py"

python "$script_path"
