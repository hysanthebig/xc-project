import anvil.files
from anvil.files import data_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import pandas as pd
import plotly.graph_objects as go
import numpy as np
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

def seconds_to_mintunes(seconds):
  mint = int(seconds // 60)
  sec = round(seconds % 60, 1)
  if sec < 10:
    sec = f"0{sec}"
  time = f"{mint}:{sec}"
  return (time)

def time_to_seconds(time):
  mintunes, seconds = time.split(":")
  mintunes = int(mintunes)
  seconds = float(seconds)
  time_seconds = mintunes*60 + seconds
  return time_seconds

def average_time_helper(df_runner,last_races_to_check):
  df_runner = df_runner.sort_values(by='Date_dt', ascending = False)
  if last_races_to_check == 0:
    last_races_to_check = len(df_runner)

  df_runner = df_runner.head(last_races_to_check)
  if df_runner.shape[0] < last_races_to_check:
    return None
  total_seconds_over_period = df_runner['time_seconds'].sum()
  averageseconds = round(total_seconds_over_period / last_races_to_check,3)
  average_time = seconds_to_mintunes(averageseconds)
  return average_time



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
def filter(sort_by,runnerlist,racelist,gradelist,lengthlist):
  readmask = pd.Series(True, index=df.index)
  runner_mask = pd.Series(False, index=df.index)
  race_mask = pd.Series(False, index=df.index)
  grade_mask = pd.Series(False, index = df.index)
  length_mask = pd.Series(False,index = df.index)
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

  for length in lengthlist[0:]:
    col_data = df["Length"].astype(str)
    single_mask = col_data.str.contains(length.strip(),case = False)
    length_mask = length_mask | single_mask
  if len(lengthlist) == 0:
    length_mask = pd.Series(True,index =df.index)

  readmask = readmask & runner_mask & race_mask & grade_mask & length_mask

  df_filtered = df.loc[readmask]
  df_filtered = df_filtered.sort_values(by=[sort_by])
  df_filtered =df_filtered.to_dict(orient="records")
  return(df_filtered)

@anvil.server.callable
def pr_display(runnerlist,lengthlist,gradelist):
  filitered_df = filter("Runner",runnerlist,[],gradelist,lengthlist)
  df_pr = table_into_df(filitered_df)
  df_pr = df_pr.sort_values(by = ["time_seconds"])
  pr_df = df_pr.groupby("Runner")['time_seconds'].min().copy()
  pr_rows = df_pr[df_pr["time_seconds"] == df_pr["Runner"].map(pr_df)]
  pr_rows = pr_rows.drop(columns = ['time_seconds','Date_dt']).to_dict(orient="records")
  return(pr_rows)


@anvil.server.callable
def graphing_module(runnerlist,gradelist,lengthlist):
  filitered_df = filter("Runner",runnerlist,[],gradelist,lengthlist)
  filitered_df = table_into_df(filitered_df)
  filitered_df = filitered_df.drop(columns =['Race','Placement'])
  grouped = filitered_df.groupby("Runner")
  plot = go.Figure()
  all_y = []

  for runner, runner_df in grouped:
    runner_df["Date_dt"] = pd.to_datetime(runner_df["Date_dt"])
    runner_df = runner_df.sort_values('Date_dt')
    hover_text = [seconds_to_mintunes(s) for s in runner_df['time_seconds']]
    xvalues = runner_df["Date_dt"].dt.tz_localize(None).dt.to_pydatetime()
    yvalues = runner_df['time_seconds']/60
    all_y.extend(yvalues.tolist())
    trace = go.Scatter(x=xvalues,y=yvalues,mode="lines+markers",name=runner,text = hover_text)
    plot.add_trace(trace)
  plot.update_xaxes(
    title="Date",
    tickformat="%m/%d/%y"  # or "%b %d" for Month Day
  )
  plot.update_yaxes(ticksuffix = ":00")
  for trace in plot.data:
    trace.text = [f"Time: {seconds_to_mintunes(s)}" for s in trace.y * 60]  # or original seconds
    trace.hovertemplate = "Race Date %{x}<br>%{text}"

  return plot

  ############################works, but use groupme
@anvil.server.callable
def average_time(runners,last_races_to_check,races_included):
  average_collected_time = {}
  df = filter("Date_dt",runners,races_included,[],[])
  df = table_into_df(df)
  for runner,df in df.groupby('Runner'):
    if average_time_helper(df,last_races_to_check) is not None:
      average_collected_time[runner] = average_time_helper(df,last_races_to_check)
  if last_races_to_check == 0:
    last_races_to_check = len(races_included)
  return_amount_of_races = last_races_to_check
  average_collected_time = sorted(average_collected_time.items())
  return average_collected_time,return_amount_of_races

@anvil.server.callable
def optimal_varisity_lineup(runner,races_to_check,races):
  average_times,x = average_time(runner,races_to_check,races)
  average_times = sorted(average_times, key = lambda x: time_to_seconds(x[1]))
  top7 = average_times[:7]
  jvnext7 = average_times[7:14]
  return top7,jvnext7

@anvil.server.callable
def comparison_between_races(runner,races):
  df = filter("Date_dt",runner,races,[],[])
  df = table_into_df(df)
  if df.shape[0] != 2:
    return None,None,None
  time_1,time_2 = df['time_seconds']
  time_difference = (time_1 - time_2)
  df["Date_dt"] = pd.to_datetime(df["Date_dt"])
  time_since = df.loc[df.index[0],"Date_dt"]-df.loc[df.index[1],"Date_dt"]
  time_since = abs(time_since.days)
  if time_since != 0:
    average_time_per_day = round(abs(time_difference)/time_since,4)
  else:
     average_time_per_day = 0
  time_difference = seconds_to_mintunes(time_difference)
  return time_difference, time_since,average_time_per_day
