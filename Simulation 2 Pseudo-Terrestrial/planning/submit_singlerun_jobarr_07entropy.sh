#!/bin/bash
#SBATCH -A e32704
###SBATCH -p normal
#SBATCH -p short
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem-per-cpu=100M
#SBATCH -t 01:00:00
#SBATCH --array=4-4
#SBATCH --job-name="jobarr_0.7_test"
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
SCRIPT_PATH="/projects/e32704/andy/decisionmaking/gridworld-decisionmaking/Simulation 2 Pseudo-Terrestrial/planning/main_singlerun_jobarr.py"
ENTROPY_LEVEL="07"
OCCLUSIONS_PATH="/projects/e32704/andy/decisionmaking/gridworld-decisionmaking/Simulation 2 Pseudo-Terrestrial/planning/Data2/Simulation_0/Occlusion_0/OcclusionCoordinates.csv"
EPISODES_PATH="/projects/e32704/andy/decisionmaking/gridworld-decisionmaking/Simulation 2 Pseudo-Terrestrial/planning/Data2/Simulation_0/Occlusion_0/Predator_0/Depth_100/Episode_0.csv"


python "$SCRIPT_PATH" \
    --data_id "$ENTROPY_LEVEL" \
    --jobarr_id $SLURM_ARRAY_TASK_ID \
    --occlusions "$OCCLUSIONS_PATH" \
    --episodes "$EPISODES_PATH" \