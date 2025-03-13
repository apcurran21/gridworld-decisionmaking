### Questions
* I'm not sure if `numWorkers` or the length of `tasks` is larger
* Apparently Monte Carlo Tree Search (MCTS) is able to be parallelized
    * I don't think that the current planning code is taking advantage of this?

## Code Overview
List of notable classes:
* History
* Game
* MCTS
* Belief 

### Notes
* The history information is stored inside the `History` class's `HistoryVector` variable, which is just a list
    * To add to this History tracker, you call `History.Add(self, action observation=-1, state=None)`. This appends an `ENTRY` instance composed of an action, observation, and state to `HistoryVector`.

### Important Functions
* `Game.MakeObservation(self, state, action)` in 'game.py'
    * will likely need to edit this function to introduce audio observations
    * one thing this function does is check the prey's visual cone to see if the predator is visible
* `Game.PredatorAgentPosPropogation(self, state)` in 'game.py'
    * this function interacts with the prey's belief state
* `Game.DisplayBeliefs(self, beliefState)` in 'game.py'
    * this looks like either a visualization or debug of the given belief state
* `Experiment.DiscountedReturn(self, occlusions, predatorHome, knowledge, occlusionInd, predatorInd, simulationDirectory, visualRange=None)` in 'experiment.py'
    * This seems to be the main "run" function within MultiExperiment




## General Notes
* the `gen_init_vars` function in 'new_main.py' sets the output directory for the planning simulations as `os.getcwd`.
* I experienced an OSError for the following job:
    * srun job start: Sun Mar  9 19:15:32 CDT 2025
        * Job ID: 7686465
    * Since it wasn't a ValueError or IndexError, `SafeMultiExperiment` did not catch it.
    * Because it wasn't safely caught, I'm unsure if execution ever progressed within the worker thread to the point where it signals being "done" back to the master thread. 
    * Here is the error and relevant traceback:
        * OSError: Cannot save file into a non-existent directory: '/projects/e32704/andy/decisionmaking/gridworld-results/initial_test/Data/Simulation_0/Occlusion_0/Predator_0'
        * Traceback (most recent call last):
            * File "/projects/e32704/andy/decisionmaking/gridworld-decisionmaking/Simulation 2 Pseudo-Terrestrial/planning/new_main.py", line 308, in <module>
                * SafeMultiExperiment(task)
            * File "/projects/e32704/andy/decisionmaking/gridworld-decisionmaking/Simulation 2 Pseudo-Terrestrial/planning/new_main.py", line 67, in SafeMultiExperiment
                * MultiExperiment(args)
            * File "/projects/e32704/andy/decisionmaking/gridworld-decisionmaking/Simulation 2 Pseudo-Terrestrial/planning/new_main.py", line 95, in MultiExperiment
                * _ = experiment.DiscountedReturn(occlusions, predatorHome, knowledge,
            * File "/projects/e32704/andy/decisionmaking/gridworld-decisionmaking/Simulation 2 Pseudo-Terrestrial/planning/experiment.py", line 169, in DiscountedReturn
                * df.to_csv(summaryFile, encoding='utf-8', index=False)
    * However, the actually file structure only has the path '/projects/e32704/andy/decisionmaking/gridworld-results/initial_test/Data/Simulation_0/Occlusion_0'
        * in other words, the 'Predator_0' directory was not created - I'm not sure yet which function is responsible for handling this
    * NOTE that the global variable `visualRange` is set to None in 'new_main.py'
    * this was the memory usage of the trial:
        * Job ID: 7686465
        * Cluster: quest
        * User/Group: apc6353/apc6353
        * State: TIMEOUT (exit code 0)
        * Nodes: 1
        * Cores per node: 2
        * CPU Utilized: 00:00:01
        * CPU Efficiency: 0.00% of 1-06:10:56 core-walltime
        * Job Wall-clock time: 15:05:28
        * Memory Utilized: 388.66 MB
        * Memory Efficiency: 1.19% of 32.00 GB
    * Note that 'OcclusionCoordinates.csv' was empty - I take this to mean that the first trial was a simple, open arena.

### Planning
* 

### Todos
* Examine the Master process code in new_main.py, as this creates the task arguments which get passed to the worker processes.
    * Note that this is all different from the init_vars.pkl creation/processing


### Experiment setup
```python
occlusionInd = args[0][0]
occlusions = args[0][1]
predatorInd = args[1][0]
predatorHome = args[1][1]
visualRange = args[2]
simulationInd = args[3]
directory = args[4]
```