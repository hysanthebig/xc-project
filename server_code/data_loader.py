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
pd.set_option('display.max_columns',None)
pd.set_option('display.width',None)
pd.set_option('display.max_rows',None)

@anvil.server.callable
def import_csf_to_table():
  with anvil.files.data_files.open("track_data.csv") as f:
    df = pd.read_csv(f)
  print(df.head)
  for _, row in df.iterrows():
    row= {k:(None if pd.isna(v) else v) for k,v in row.items()}
    exists = app_tables.track_table.search(Runner=row["Runner"],Race=row["Race"],RaceType=row["RaceType"])
    if not list(exists):
      app_tables.track_table.add_row(
        Runner=row["Runner"],Race=row["Race"],Placement=row["Placement"],Grade=row["Grade"],Time=row["Time"],Avr_splits=row["Avr splits"],Date=row["Date"],Length=row["Distance"],RaceType = row["RaceType"],Date_dt=row["Date_dt"],time_seconds=row["time_seconds"])
  return "Done"

def sort_table_by_first_name_inplace(table, data_grid):
  rows = list(table.search())
  rows_with_first = []
  for row in rows:
    runner = row.get('Runner', '')
    if "," in runner:
      last, first = runner.split(",", 1)
      runner = f"{first.strip()} {last.strip()}"
    first_name = runner.split()[0] if runner else ""
    rows_with_first.append((row, first_name))
  rows_with_first.sort(key=lambda x: x[1].lower())
  data_grid.items = [row for row, _ in rows_with_first]
  return "DataGrid updated by first name"

  sort_table_by_first_name_inplace(app_tables.track_table)