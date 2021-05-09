import numpy as np
import pandas as pd 
import datetime
import random
import itertools as it

class Task():
  def __init__(self, Name, DateTime=None, EstimatedTime=None, Effort=None, Frequency=None, FunFactor=None):
    self._name = Name 
    self._estimated_time = EstimatedTime #Estimated total time for task in minutes
    self._effort = Effort #Effort per minute for task (From 1 to 10)
    self._frequency = Frequency #How often the user is ok with doing the task (2 = every other, 1 = every day)
    self._fun_factor = FunFactor #Ammount of fun per minute for task (From 1 to 10)
    self._datetime = DateTime #When the task should be done (in date-time object)
  
  @property
  def name(self):
    return self.name

  @property
  def estimated_time(self):
    return self.estimated_time
    
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
  def datetime(self):
    return self._datetime

  def __sizeof__(self):
    return self._estimated_time
  

class Schedule():
  """Class Schedule: Schedules your week :)"""
  def __init__(self, tasks=None):
    self._tasks = []
    self._schedule = pd.DataFrame(columns=["Date", "Time"])
    self.add_task(task)
      
  def add_task(self, task):
    if task != None:
      self._tasks.append(task)
      

  def optimize_current(self):
    "Function: Optimizes current tasks in Schedule class."
    pass
  
  def spread_evenly(self, chunks, lst = self._tasks):
    "Function: Evenly distributes task, taking estimated time as factor."
    time_to_plan = 0   
    temp_lst = []
    for i in lst:
      time_to_plan += i.estimated_time
      temp_lst.append(i.estimated_time)
    time_to_plan = time_to_plan / chunks
    for i in lst:
      temp_lst.append(i.est)
    best_spread = []
    for i in it.combinations(lst, time_to_plan):
      print(i)
    # stop = False
    # while not stop:
    #   tasks = lst.copy()
    #   days = []
    #   for i in range(chunks):
    #     days.append[[]]
        
    #   for day in days:
    #     for task in tasks:
      

    
      
  def spread_evenly(self, chunks, lst = self._tasks):
    "Function: Evenly distributes task, taking estimated time as factor." 
    tasks = lst.copy()
    tasks.sort()
    
    days = []
    for _ in range(chunks):
      days.append[[]]
      
    while tasks != []:
      task = task.pop(-1)

      for day in days:
        sizeofDay = lambda()
    

      

  
  def __str__(self):
    print(self._schedule)
    
  def __len__(self):
    return(len(self._tasks))


class Interface():
  def __init__(self):
    self._schedule = Schedule()
    self._week_days = [True, True, True, True, True, True, True]
    self._day_start = datetime.time(hour=8)
    self._day_stop = datetime.time(hour=17)
  
  def main_menu(self):
    print("""
          1. Setup week
          2. Add task
          3. Optimize schedule
          4. Show schedule
          5. Export schedule
          """)
    choice = input("Select an option: ")
    try:
      choice = int(choice)
    except TypeError:
      print("Please type a number")
      return self.main_menu()
    if choice not in [1, 2, 3, 4, 5]:
      print("Please select one of the provided options")
      return self.main_menu()
    
    if choice == 1:
      setup_week()
    elif choice == 2:
      add_task()
    elif choice == 3:
      optimize_schedule()
    elif choice == 4:
      show_schedule()
    else:
      export_schedule()
    
  def setup_week():
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
        while running:
          print(f"Use {d(day)}?")
          val = input("y/n?: ")
          if val = "y":
            self._week_days[day] = True
            running = False
          elif val = "n":
            self._week_days[day] = False
            running = False
          else:
            print("Please use inputs 'y' or 'n'")
    else:
      print("What time do you want to start your day?")
      self._day_start = _get_user_time()
      print("What time do you want to stop your day?")
      self._day_start = _get_user_time()
  
  def _get_user_time():
    print("Use format HH:MM")
    val = input("Time: ")
    try:
      value = datetime.datetime.strptime(val, "%H:%M")
      return value
    except:
      print("Please use the provided time format")
      return _get_user_time()
  
  def add_task():
    print("What is your task name?")
    name = input("Name: ")
    print("How much effort is there (1-10)? (Press enter to skip)")
    effort = input("Effort: ")
    if effort != "":
      try:
        effort = int(choice)
      except TypeError:
        print("Please type a number")
        return 
      if effort not in range(1, 11):
        print("Please select one of the provided options")
        return 
  
  def optimize_schedule():
    pass
  
  def show_schedule():
    pass
  
  def export_schedule():
    pass
  

if __name__ == "__main__":
  print(":)")
  Sched = Schedule()