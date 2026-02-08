from ._anvil_designer import Form1Template
from anvil import *
import plotly.graph_objects as go
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server


class Form1(Form1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    self.repeating_panel_1.items = [
      {'Runner':'Waylon'}]

    # Any code you write here will run before the form opens.



  
  def main_data_display(self):
    self.repeating_panel_1.items = anvil.server.call('get_data_rows')
    
  def data_refresh(self,**event_args):
    self.main_data_display()
    
  @handle("import_csv_to_datattable", "click")
  def import_csv_to_datattable_click(self, **event_args):
      anvil.server.call('import_csf_to_table')
  
  @handle("refreshtest", "click")
  def refreshtest_click(self, **event_args):
      data_refresh(self,**event_args)

