import numpy as np
import pandas as pd 
import datetime
import random
import itertools as it
from knapsack_solver import knapsack

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
  

class Schedule():
  """Class Schedule: Schedules your week :)"""
  def __init__(self, tasks=None):
    self._tasks = []
    self._schedule = pd.DataFrame(columns=["Date", "Time"])
      
  def add_task(self, task):
    if task != None:
      time = task.estimated_time
      for i in range(time):
        if task.time != None:
          temp = Task(task.name, Date=task.date, Time=task.time+i, EstimatedTime=1, Effort=task.effort, Frequency=1, FunFactor=task.fun_factor)
          self._tasks.append(temp)
        else:
          temp = Task(task.name, Date=task.date, Time=task.time, EstimatedTime=1, Effort=task.effort, Frequency=1, FunFactor=task.fun_factor)
          self._tasks.append(temp)
  
  # def spread_evenly(self, chunks, lst, occupied = None):
  #   "Function: Evenly distributes task, taking estimated time as factor."
  #   sorted_list = sort(lst).copy()
  #   days = []
  #   if occupied:
  #     days = occupied
  #   else:
  #     days = [[] for _ in range(chunks)]
  #   while sorted_list:
  #     min = days[0]
  #     for i in days[1:]:
  #       if i.sum < min.sum:
  #         min = i
  #     min.append(sorted_list.pop())
  #   return days
      
  def setup_sched(self):
    self._schedule = pd.DataFrame(index=range(24))
    for i in range(7):
      self._schedule[i] = "Empty"
    
      
  def spread_evenly(self, dates, lst=None):
    "Function: Evenly distributes task, taking estimated time as factor."
    if lst == None:
      lst = self._tasks
    
    days = []
    for date in dates:
      days.append({"Date": date, "Tasks": [], "Size": 0})
    
    for task in lst:
      for day in days:
        if task.date == day["Date"]:
          day["Tasks"].append(task)
          lst.remove(task)
          
    tasks = lst.copy()
    tasks.sort()
      
    while tasks != []:
      task = task.pop(-1)

      for day in days:
        for element in day["Tasks"]:
          day["Size"] += element.estimated_time
      
      smallestday = days[0]
      for day in days:
        if day["Size"] <= smallestday["Size"]:
          smallestday = day

      smallestday["Tasks"].append(task)

    return days
  
  def optimize_current(self, sizeofDay, amountOfDays):
    "Function: Optimizes current tasks in Schedule class."
    self.solver = knapsack()
    return(self.solver.main(self._tasks, amountOfDays, sizeofDay))
    
  
  def fitness(individual, data):
    pass
  
  def __str__(self):
    print(self._schedule)
    
  def __len__(self):
    return(len(self._tasks))


class Interface():
  def __init__(self):
    self._schedule = Schedule()
    self._week_days = [True, True, True, True, True, True, True]
    self._day_start = 8
    self._day_stop = 17
    self._main_running = True
    self._scheduled_days = None
  
  def main_menu(self):
    while self._main_running:
      print("""
            1. Setup week
            2. Add task
            3. Optimize schedule
            4. Show schedule
            5. Export schedule
            6. Exit Program
            """)
      choice = input("Select an option: ")
      try:
        choice = int(choice)
      except TypeError:
        print("Please type a number")
        return self.main_menu()
      if choice not in [1, 2, 3, 4, 5, 6]:
        print("Please select one of the provided options")
        return self.main_menu()
      
      if choice == 1:
        self.setup_week()
      elif choice == 2:
        self.add_task()
      elif choice == 3:
        self.optimize_schedule()
      elif choice == 4:
        self.show_schedule()
      elif choice == 5:
        self.export_schedule()
      else:
        self._main_running = False

  def setup_week(self):
    print("""
          1. Select used days
          2. Set day length
          """)
    choice = input("Select an option: ")
    try:
      choice = int(choice)
    except TypeError:
      print("Please type a number")
      return self.setup_week()
    if choice not in [1, 2]:
      print("Please select one of the provided options")
      return self.setup_week()
    
    d = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
    if choice == 1:
      print("""
            Select the days that you want to use
            """)
      running = True
      for day in range(7):
        running = True
        while running:
          print(f"Use {d[day]}?")
          val = input("y/n?: ")
          if val == "y":
            self._week_days[day] = True
            running = False
          elif val == "n":
            self._week_days[day] = False
            running = False
          else:
            print("Please use inputs 'y' or 'n'")
    else:
      print("What time do you want to start your day?")
      self._day_start = self._get_user_time()
      print("What time do you want to stop your day?")
      self._day_start = self._get_user_time()
  
  def _get_user_time(self):
    print("Select hour")
    val = input("Time: ")
    
    value = _check_num(val)
    if value != None:
      return value

  
  def add_task(self):
    print("What is your task name?")
    name = input("Name: ")
    if name == "":
      print("Please provide a name")
      return
    
    print("What is the expected time the task will take?")
    est_time = input("Time: ")
    if est_time != "":
      est_time = abs(self._check_num(est_time))
    else:
      print("Please provide a name")
      return
    
#    print("Does your task run on a specific day? (0-6) (Press enter to skip)")
#    day = input("Day: ")
#    if day != "":
#      day = self._check_num(day, range(1, 7))
#    else:
#      day = None
#    
#    print("Does your task run on a specific time? (Hour) (Press enter to skip)")
#    time = input("Fun factor: ")
#    if time != "":
#      time = self._check_num(time, range(0, 24))
#    else:
#      time = None
    
    print("How much effort is there (1-10)? (Press enter to skip)")
    effort = input("Effort: ")
    if effort != "":
      effort = self._check_num(effort, range(1, 11))
    else:
      effort = None
    
#    print("How many times should this task be repeated (Press enter to skip)")
#    frequency = input("Repeats: ")
#    if frequency != "":
#      frequency = abs(self._check_num(frequency, range(1, 8)))
#    else:
#      frequency = None
    
    print("How fun is the task (1-10)? (Press enter to skip)")
    fun = input("Fun factor: ")
    if fun != "":
      fun = self._check_num(fun, range(1, 11))
    else:
      fun = None
    
    
    task = Task(Name=name, EstimatedTime=est_time, Effort=effort, FunFactor=fun)
    self._schedule.add_task(task)
  
  def _check_num(self, val, options=None):
    try:
      val = int(val)
      return val
    except TypeError:
      print("Please type a number")
      return None
    if options != None and effort not in options:
      print("Please use one of the provided options")
      return None
  
  def optimize_schedule(self):
    print("Starting optimization!")
    self._scheduled_days = self._schedule.optimize_current(self._day_stop - self._day_start, sum(self._week_days))
    print("Optimization finished!")
  def show_schedule(self):
    if self._scheduled_days != None:
      self._schedule.solver.print_sched(self._scheduled_days)
    else:
      print("Please solve before using")
  
  def export_schedule(self):
    pass
  

if __name__ == "__main__":
  print(":)")
  # Sched = Schedule()
  UI = Interface()
  UI.main_menu()