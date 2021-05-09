from ortools.linear_solver import pywraplp
import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class Task():
  def __init__(self, Name, Date=None, Time=None, EstimatedTime=None, Effort=None, Frequency=1, FunFactor=None):
    self._name = Name 
    self._estimated_time = EstimatedTime #Estimated total time for task in minutes
    self._effort = Effort #Effort per minute for task (From 1 to 10)
    self._frequency = Frequency #How often the user is ok with doing the task (2 = every other, 1 = every day)
    self._fun_factor = FunFactor #Ammount of fun per minute for task (From 1 to 10)
    self._time = Time #When the task should be done (in date-time object)
    self._date = Date
  
  @property
  def name(self):
    return self._name

  @property
  def estimated_time(self):
    return self._estimated_time
    
  @property
  def effort(self):
    return self._effort
    
  @property
  def frequency(self):
    return self._frequency

  @property
  def fun_factor(self):
    return self._fun_factor
    
  @property
  def date(self):
    return self._date
    
  @property
  def time(self):
    return self._time

  def __sizeof__(self):
    return self._estimated_time





class knapsack:
    
    
    def create_data_model(self, ilst, bins, capacity):
        lst = ilst.copy()
        if len(lst) < bins * capacity:
            padding = bins * capacity - len(lst)
            for i in range(padding):
                lst.append(Task(f"Freetime", None, None, 1, 1, 1, 1))
        
        data = {}
        estimated_time = [_.estimated_time for _ in lst]
        effort = [_.effort for _ in lst]
        funFactor = [_.fun_factor+10 for _ in lst]
        data["time"] = estimated_time
        data["effort"] = effort
        data["funFactor"] = funFactor
        data["bins"] = list(range(bins))
        data["num_items"] = len(lst)
        data["capacity"] = [capacity for _ in range(bins)]
        data["tasks"] = [_.name for _ in lst]
        data["items"] = list(range(len(lst)))
        
        # if len(lst) < bins * capacity:
        #     for i in range(bins * capacity - len(lst)):
        #         data["time"].append(1)
        #         data["effort"].append(1)
        #         data["funFactor"].append(11)
        #         data["tasks"].append("Freetime")
        #         data["items"].append(len(lst)+i)
                
        return data
    
    def main(self, lst, bins, capacity):
        data = self.create_data_model(lst, bins, capacity)

        solver = pywraplp.Solver.CreateSolver("SCIP")

        x = {}
        for i in data["items"]:
            for j in data["bins"]:
                x[(i, j)] = solver.IntVar(0, 1, "x_%i_%i" % (i, j))
        
        for i in data["items"]:
            solver.Add(sum(x[i, j] for j in data["bins"]) <= 1)
        
        for j in data["bins"]:
            solver.Add(sum(x[(i, j)] * data["time"][i]
                    for i in data["items"]) <= data["capacity"][j])

        objective = solver.Objective()

        for i in data['items']:
            for j in data['bins']:
                objective.SetCoefficient(x[(i, j)], data["funFactor"][i] - data["effort"][i])
                #objective.SetCoefficient(x[(i, j)], data["effort"][i])
        objective.SetMaximization()

        status = solver.Solve()

        own_x = []

        if status == pywraplp.Solver.OPTIMAL:
            print('Total packed value:', objective.Value())
            total_time = 0
            for j in data['bins']: #from 0 to 6
                own_x.append([])
                bin_time = 0
                bin_feffort = 0
                print('Day ', j+1, '\n')
                for i in data['items']: #from 0 to 56
                    if x[i, j].solution_value() > 0:
                        own_x[j].append(data["tasks"][i])
                        print('Item', i, '- time:', data['time'][i], ' fun - effort:', max(data["funFactor"][i] - data["effort"][i],1))
                        bin_time += data['time'][i]
                        bin_feffort += data["funFactor"][i] - data["effort"][i]
                print('Day time:', bin_time)
                print('Day fun - effort:', bin_feffort)
                print()
                total_time += bin_time
            print('Total packed weight:', total_time)
        else:
            print('The problem does not have an optimal solution.')
        return own_x
        

    def print_sched(self, data_list):
        df = pd.DataFrame(data_list)
        
        print(df.T)
        #return df.T
        
# Name, Date=None, Time=None, EstimatedTime=None, Effort=None, Frequency=1, FunFactor=None):

if __name__ == "__main__":
    solver = knapsack()
    tasks = []
    for i in range(100):
        tasks.append(Task(f"Work {i}", None, None, random.randint(1, 5), random.randint(1, 10), 1, random.randint(1, 10)))

    # for i in range(46):
    #     tasks.append(Task(f"Sleep", None, None, 1, 1, 1, 1))
    data_list = solver.main(tasks, 5, 20) # days, hours
    
    solver.print_sched(data_list)
    #plt.hist(df)
    #plt.show()
    #plt.hist(df, bins = 20)
    #plt.show()