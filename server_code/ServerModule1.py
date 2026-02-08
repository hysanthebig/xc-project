import anvil.files
from anvil.files import data_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import pandas as pd
# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
# @anvil.server.callable
# def say_hello(name):
#   print("Hello, " + name + "!")
#   return 42
#
rows = app_tables.datatable.search()
data_list = []
for r in rows:
  data_list.append({
    "Runner": r["Runner"],
    "Race": r["Race"],
    "Grade": r["Grade"],
    "Placement":r["Placement"],
    "Date":r["Date"],
    "Date_dt":r["Date_dt"],
    "Time":r["Time"],
    "time_seconds":r["time_seconds"],
    "Length":r["Length"],
    "Avr_splits":r['Avr_splits']
  })
df = pd.DataFrame(data_list)


@anvil.server.callable
def one_of_item():
  rows = app_tables.datatable.search()
  one_runner = sorted(set(row['Runner'] for row in rows))
  one_race = sorted(set(row['Race'] for row in rows))
  one_grade =sorted(set(row['Grade']for row in rows))
  return(one_runner,one_race, one_grade)

@anvil.server.callable
def filter(sort_by,runnerlist,racelist,gradelist):
  readmask = pd.Series(True, index=df.index)
  runner_mask = pd.Series(False, index=df.index)
  race_mask = pd.Series(False, index=df.index)
  grade_mask = pd.Series(False, index = df.index)
  
  for runner in runnerlist[0:]:
    col_data = df["Runner"].astype(str)
    single_runner_mask = col_data.str.contains(runner.strip(),case = False)
    runner_mask = runner_mask | single_runner_mask
  if len(runnerlist) == 0:
      runner_mask = pd.Series(True,index =df.index)

  for race in racelist[0:]:
    col_data = df["Race"].astype(str)
    single_mask = col_data.str.contains(race.strip(),case = False)
    race_mask = race_mask | single_mask
  if len(racelist) == 0:
    race_mask = pd.Series(True,index =df.index)

  for grade in gradelist[0:]:
    col_data = df["Grade"].astype(str)
    single_mask = col_data.str.contains(str(grade))
    grade_mask = grade_mask | single_mask
  if len(gradelist) == 0:
    grade_mask = pd.Series(True,index =df.index)

  readmask = readmask & runner_mask & race_mask & grade_mask

  df_filtered = df.loc[readmask]
  df_filtered = df_filtered.sort_values(by=[sort_by])
  df_filtered =df_filtered.drop(columns = ['time_seconds','Date_dt']).to_dict(orient="records")
  return(df_filtered)