import time
from ortools.sat.python import cp_model


class VarArrayAndObjectiveSolutionPrinter(cp_model.CpSolverSolutionCallback):
    def __init__(self, variables, limit):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__variables = variables
        self.__solution_count = 0
        self.__solution_limit = limit
        self.solution_list = []
        self.solution_time = []
        self.solution_objective = []
        self.best_bound = 0
        self.__start_time = time.time()

    def on_solution_callback(self):
        self.__solution_count += 1
        if self.__solution_count >= self.__solution_limit:
            self.StopSearch()
        self.solution_list.append([self.Value(v) for v in self.__variables])
        current_time = time.time()
        obj = self.ObjectiveValue()
        self.best_bound = self.BestObjectiveBound()
        self.solution_time.append(current_time - self.__start_time)
        self.solution_objective.append(obj)

    def solution_count(self):
        return self.__solution_count
