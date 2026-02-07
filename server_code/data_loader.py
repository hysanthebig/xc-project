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
@anvil.server.callable
def import_csf_to_table():
  with anvil.files.data_files.open("xc_data.csv") as f:
    df = pd.read_csv(f)

  for _, row in df.iterrows():
    row= {k:(None if pd.isna(v) else v) for k,v in row.items()}
    app_tables.datatable.add_row(
      Runner=row["Runner"],Race=row["Race"],Placement=row["Placement"],Grade=row["Grade"],Time=row["Time"],Avr_splits=row["Avr splits"],Date=row["Date"],Length=row["Length"],Date_dt=row["Date_dt"],time_seconds=row["time_seconds"])
  return "Done"
  