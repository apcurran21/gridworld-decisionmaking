from mcts import MCTS, SearchParams
from episode import Episode
from timeit import default_timer as timer
from statistics0 import STATISTICS

import csv, pickle, os

from pathlib import Path
import pandas as pd

class Results:
    def __init__(self):
        self.Time = STATISTICS(0., 0.)
        self.Reward = STATISTICS(0., 0.)
        self.DiscountedReturn = STATISTICS(0., 0.)
        self.UndiscountedReturn = STATISTICS(0., 0.)
        self.Steps = STATISTICS(0., 0.)

    def Clear(self):
        self.Time.Clear()
        self.Reward.Clear()
        self.DiscountedReturn.Clear()
        self.UndiscountedReturn.Clear()
        self.Steps.Clear()


class ExperimentParamsOld:
    SpawnArea = 4
    NumRuns = 20
    NumPredators = 5
    NumSteps = 200
    SimSteps = 1000
    TimeOut = 36000
    MinDoubles = 0
    MaxDoubles = 50
    TransformDoubles = -1
    TransformAttempts = 1000
    Accuracy = 0.01
    UndiscountedHorizon = 100
    AutoExploration = True
    EntropyLevels = [float(i)/10. for i in range(0, 10)]
    Depth = [100, 1000, 5000]

    def __str__(self):
        return (f"ExperimentParams:\n"
                f"\tSpawnArea: {self.SpawnArea}\n"
                f"\tNumRuns: {self.NumRuns}\n"
                f"\tNumPredators: {self.NumPredators}\n"
                f"\tNumSteps: {self.NumSteps}\n"
                f"\tSimSteps: {self.SimSteps}\n"
                f"\tTimeOut: {self.TimeOut}\n"
                f"\tMinDoubles: {self.MinDoubles}\n"
                f"\tMaxDoubles: {self.MaxDoubles}\n"
                f"\tTransformDoubles: {self.TransformDoubles}\n"
                f"\tTransformAttempts: {self.TransformAttempts}\n"
                f"\tAccuracy: {self.Accuracy}\n"
                f"\tUndiscountedHorizon: {self.UndiscountedHorizon}\n"
                f"\tAutoExploration: {self.AutoExploration}\n"
                f"\tEntropyLevels: {self.EntropyLevels}\n"
                f"\tDepth: {self.Depth}\n")


class ExperimentParams:
    # my edits to decrease the number of total simulations
    SpawnArea = 4
    NumRuns = 1
    NumPredators = 1
    NumSteps = 100
    SimSteps = 1000
    TimeOut = 3600
    MinDoubles = 0
    # MaxDoubles = 5      # should be 5 trials
    MaxDoubles = 1
    TransformDoubles = -1
    TransformAttempts = 1000
    Accuracy = 0.01
    UndiscountedHorizon = 100
    AutoExploration = True
    # EntropyLevels = [float(i)/10. for i in range(0, 10, 3)]
    # EntropyLevels = [0.5] # only one entropy level, and high entropy
    EntropyLevels = [0.7] # only one entropy level, and high entropy
    # i believe that hearing will be more helpful at this level of clutter
    Depth = [100]   # only the most shallow thinking for computational reasons

    def __str__(self):
        return (f"ExperimentParams:\n"
                f"\tSpawnArea: {self.SpawnArea}\n"
                f"\tNumRuns: {self.NumRuns}\n"
                f"\tNumPredators: {self.NumPredators}\n"
                f"\tNumSteps: {self.NumSteps}\n"
                f"\tSimSteps: {self.SimSteps}\n"
                f"\tTimeOut: {self.TimeOut}\n"
                f"\tMinDoubles: {self.MinDoubles}\n"
                f"\tMaxDoubles: {self.MaxDoubles}\n"
                f"\tTransformDoubles: {self.TransformDoubles}\n"
                f"\tTransformAttempts: {self.TransformAttempts}\n"
                f"\tAccuracy: {self.Accuracy}\n"
                f"\tUndiscountedHorizon: {self.UndiscountedHorizon}\n"
                f"\tAutoExploration: {self.AutoExploration}\n"
                f"\tEntropyLevels: {self.EntropyLevels}\n"
                f"\tDepth: {self.Depth}\n")
    


class Experiment:
    def __init__(self, real, simulator, jobarr_id):
        self.JobArrID = jobarr_id
        self.Real = real
        self.Simulator = simulator
        self.Episode = Episode()

        if ExperimentParams.AutoExploration:
            if SearchParams.UseRave:
                SearchParams.ExplorationConstant = 0
            else:
                SearchParams.ExplorationConstant = self.Simulator.GetRewardRange()

        self.Results = Results()
        MCTS.InitFastUCB(SearchParams.ExplorationConstant)

    def Run(self):
        notOutOfParticles = True
        undiscountedReturn = 0.0
        discountedReturn = 0.0
        discount = 1.0

        state = self.Real.CreateStartState()
        currentState = self.Real.Copy(state)
        self.Episode.Add(-1, -1, currentState, -1, 0)   # since action and observation are not defined for the start state (-1),
                                                        # do the same for the audio observation

        self.MCTS = MCTS(self.Simulator)

        start = timer()
        t = 0
        observation = 0
        self.NumObservation = 0


        while t < ExperimentParams.NumSteps:
            action = self.MCTS.SelectAction(state)

            terminal, state, observation, reward, audio_observation = self.Real.Step(state, action)
            currentState = self.Real.Copy(state)

            self.NumObservation += 1*(observation > 0)
            undiscountedReturn += reward
            discountedReturn += reward * discount
            discount *= self.Real.GetDiscount()

            self.Episode.Add(action, observation, currentState, audio_observation, reward)

            if SearchParams.Verbose:
                self.Real.DisplayState(state)

            if terminal:
                self.Episode.Add(action, observation, currentState, audio_observation, reward)
                self.Episode.Complete()
                return reward

            notOutOfParticles, beliefState = self.MCTS.Update(action, observation, currentState)
            if not notOutOfParticles:
                print("random action selection")
                self.Episode.Add(action, observation, currentState, audio_observation, reward)
                break

#            if (timer() - start) > ExperimentParams.TimeOut:
#                break

            t += 1

        if not notOutOfParticles:
            if SearchParams.Verbose:
                print("Out of particles, finishing episode with SelectRandom")
            history = self.MCTS.GetHistory()

            while t <= ExperimentParams.NumSteps:
                t += 1

                action = self.Simulator.SelectRandom(state, history, self.MCTS.GetStatus())
                terminal, state, observation, reward, audio_observation = self.Real.Step(state, action)

                self.Results.Reward.Add(reward)
                undiscountedReturn += reward
                discountedReturn += reward * discount
                discount *= self.Real.GetDiscount()

                if SearchParams.Verbose:
                    self.Real.DisplayState(state)

                if terminal:
                    self.Episode.Add(action, observation, state, audio_observation, reward)
                    self.Episode.Complete()
                    return reward

                self.MCTS.History.Add(action, observation)
                self.Episode.Add(action, observation, state, audio_observation, reward)

    def DiscountedReturn(self, occlusions, predatorHome, knowledge,
                                    occlusionInd, predatorInd, simulationDirectory, visualRange=None):

        occlusionDirectory = simulationDirectory + '/Occlusion_%d'%(occlusionInd)
        Path(occlusionDirectory).mkdir(parents=True, exist_ok=True)
        occlusionFile = occlusionDirectory + '/OcclusionCoordinates.csv'
        if not Path(occlusionFile).is_file():
            self.OcclusionCoords2CSV(occlusions, occlusionFile)

        if visualRange is None:
            summaryFile = simulationDirectory + '/Occlusion_%d/Predator_%d/Summary.csv' % (occlusionInd, predatorInd)
        else:
            summaryFile = simulationDirectory + '/Occlusion_%d/Predator_%d/VisualRange_%d/Summary.csv' % \
                          (occlusionInd, predatorInd, visualRange)

        summary = {'Depth 100': [],
                   'Depth 1000': []}

        # TODO: this is weird
        # I think this might be an artifact of their attempts at rerunning something:
        # eg, if the summary file exists, they knew that they already had their 100 and 1000
        # depth runs, so they just needed to run the 5000 depth runs
        # if Path(summaryFile).is_file():
        #     ExperimentParams.Depth = [5000]

        for depth in ExperimentParams.Depth:
            print(f"current depth: {depth}")
            if visualRange is None:
                directory = simulationDirectory + '/Occlusion_%d/Predator_%d/Depth_%d' % (occlusionInd, predatorInd, depth)
                Path(directory).mkdir(parents=True, exist_ok=True)
            else:
                directory = simulationDirectory + '/Occlusion_%d/Predator_%d/VisualRange_%d/Depth_%d' % (
                occlusionInd, predatorInd, visualRange, depth)
                Path(directory).mkdir(parents=True, exist_ok=True)

            for trial in range(ExperimentParams.MinDoubles, ExperimentParams.MaxDoubles):
                print(f"current trial: {trial}")
                episodeFile = directory + '/Episode_%d.csv' % (trial)

                if Path(episodeFile).is_file():
                    episode = pd.read_csv(episodeFile, header=0)
                    if episode['Reward'].iloc[-1] != -1:
                        return 1

                self.Results.Clear()

                SearchParams.NumSimulations = depth
                SearchParams.NumStartState = depth
                SearchParams.Softmax = False
                if depth > 10:
                    SearchParams.Softmax = True

                if int(depth * (10 ** ExperimentParams.TransformDoubles)) > 0:
                    SearchParams.NumTransforms = int(depth * (10 ** ExperimentParams.TransformDoubles))
                else:
                    SearchParams.NumTransforms = 1

                SearchParams.Softmax = False
                SearchParams.MaxAttempts = SearchParams.NumTransforms * ExperimentParams.TransformAttempts

                if visualRange:
                    if visualRange <= 3:
                        SearchParams.MaxDepth = 50
                    if visualRange == 4:
                        SearchParams.MaxDepth = 100
                    if visualRange > 4:
                        SearchParams.MaxDepth = 200

                self.Real.__init__(self.Real.XSize, self.Real.YSize, visualrange=visualRange,
                                   occlusions=occlusions)
                self.Real.PredatorHome = predatorHome
                self.Real.SetKnowledge(knowledge)

                self.Simulator.__init__(self.Simulator.XSize, self.Simulator.YSize, visualrange=visualRange,
                                        occlusions=occlusions)
                self.Simulator.PredatorHome = predatorHome
                self.Simulator.SetKnowledge(knowledge)

                if SearchParams.Verbose:
                    self.Real.InitializeDisplay()

                terminalReward = self.Run()
                # not sure what to do with terminal reward?
                print("Trial finsished: length of episodes is ", len(self.Episode.EpisodeVector))

                self.Episode.Episode2CSV(episodeFile)

                print("After call to self.Episode.Episode2CSV, len of episode vector is ", len(self.Episode.EpisodeVector))

                self.Episode.Clear()

        print("done with call to discounted return")


    def Dictionary2CSV(self, dictTable, filename):
        columns = sorted(dictTable)
        with open(filename, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(columns)
            writer.writerows(zip(*[dictTable[col] for col in columns]))

    def OcclusionCoords2CSV(self, occlusions, occlusionFile):
        occlusionDict = {}
        occlusionDict['X'] = []; occlusionDict['Y'] = []
        for coord in occlusions:
            occlusionDict['X'].append(coord.X); occlusionDict['Y'].append(coord.Y)

        self.Dictionary2CSV(occlusionDict, occlusionFile)
