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


@anvil.server.callable
def get_data_rows():
  records = []
  for row in app_tables.datatable.search():
    records.append({
      'Runner': row['Runner'],
      'Race': row['Race'],
      'Grade': row['Grade'],
      'Placement': row['Placement'],
      'Time': row['Time'],
      'Avr_splits': row['Avr_splits'],
      'Date': row['Date'],
      'Length': row['Length'],
      'Date_dt': row['Date_dt'],
      'time_seconds': row['time_seconds']
    })
  return records

@anvil.server.callable
def one_of_runner():
  rows = app_tables.datatable.search()
  one_runner = sorted(set(row['Runner'] for row in rows))
  return(one_runner)
  