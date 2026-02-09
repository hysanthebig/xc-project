import anvil.files
from anvil.files import data_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import pandas as pd
import plotly.graph_objects as go
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

def table_into_df(rows):
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
  return(df)

df = table_into_df(rows)

@anvil.server.callable
def one_of_item():
  #############################Returns a list of single items, no repeats
  rows = app_tables.datatable.search()
  one_runner = sorted(set(row['Runner'] for row in rows))
  one_race = sorted(set(row['Race'] for row in rows))
  one_grade =sorted(set(row['Grade']for row in rows))
  one_length =sorted(set(row['Length']for row in rows))
  return(one_runner,one_race, one_grade,one_length)

@anvil.server.callable
def filter(sort_by,runnerlist,racelist,gradelist):
  readmask = pd.Series(True, index=df.index)
  runner_mask = pd.Series(False, index=df.index)
  race_mask = pd.Series(False, index=df.index)
  grade_mask = pd.Series(False, index = df.index)
  ####################Filter#######################
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
  df_filtered =df_filtered.to_dict(orient="records")
  return(df_filtered)
  
@anvil.server.callable
def pr_display(lengthlist,gradelist):
  df_pr = df.copy()
  df_pr = df_pr.sort_values(by = ["time_seconds"])
  pr_df = df_pr.groupby("Runner")['time_seconds'].min().copy()
  pr_rows = df_pr[df_pr["time_seconds"] == df_pr["Runner"].map(pr_df)]

  readmask = pd.Series(True, index=df.index)
  grade_mask = pd.Series(False, index = df.index)
  length_mask = pd.Series(False, index = df.index)
  
  for grade in gradelist[0:]:
    col_data = pr_rows["Grade"].astype(str)
    single_mask = col_data.str.contains(str(grade))
    grade_mask = grade_mask | single_mask
  if len(gradelist) == 0:
    grade_mask = pd.Series(True,index =df.index)
    
  for length in lengthlist[0:]:
    col_data = pr_rows["Grade"].astype(str)
    single_mask = col_data.str.contains(length.strip(),case = False)
    length_mask = length_mask | single_mask
  if len(lengthlist) == 0:
    length_mask = pd.Series(True,index =df.index)

  readmask = readmask & grade_mask & length_mask

  pr_rows = pr_rows[readmask]
  pr_rows = pr_rows.drop(columns = ['time_seconds','Date_dt']).to_dict(orient="records")
  return(pr_rows)
@anvil.server.callable
def graphing_module(runnerlist,gradelist):
  filitered_df = filter("Runner",runnerlist,[],gradelist)
  filitered_df = table_into_df(filitered_df)
  filitered_df = filitered_df.drop(columns =['Race','Placement'])
  grouped = filitered_df.groupby("Runner")
  plot = go.Figure()
  for runner, runner_df in grouped:
    runner_df = runner_df.sort_values('Date_dt')
    xvalues = runner_df["Date_dt"]
    yvalues = runner_df['time_seconds']
    trace = go.Scatter(x=xvalues,y=yvalues,mode="lines+markers",name=runner)
    plot = plot.add_trace(trace)
  return plot

  
  