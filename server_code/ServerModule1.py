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
def get_data_rows():
  result = df.to_dict(orient="records")
  return result

@anvil.server.callable
def one_of_runner():
  rows = app_tables.datatable.search()
  one_runner = sorted(set(row['Runner'] for row in rows))
  return(one_runner)
  