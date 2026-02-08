from ._anvil_designer import Form1Template
from anvil import *
import plotly.graph_objects as go
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from anvil import CheckBox


class Form1(Form1Template):

  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)


    self.runner_checkbox = []
    total_runner = anvil.server.call('one_of_runner')  
    checkmark_runner = CheckBox(text='All Runners',checked=True)
    self.flow_panel_1.add_component(checkmark_runner)

    for runner in total_runner:
      checkmark_runner = CheckBox(text=runner,checked=False)
      self.flow_panel_1.add_component(checkmark_runner)
      self.runner_checkbox.append(checkmark_runner)


    # Any code you write here will run before the form opens.




  def main_data_display(self):
    data =  anvil.server.call('get_data_rows')
    self.repeating_panel_1.items =data

  def get_selected_runners(self):
    selected_runners = [checkmark_runner.text for checkmark_runner in self.runner_checkbox if checkmark_runner.checked]
    if selected_runners == None:
      return
    else:
      return selected_runners


  @handle("import_csv_to_datattable", "click")
  def import_csv_to_datattable_click(self, **event_args):
    anvil.server.call('import_csf_to_table')

  @handle("refreshtest", "click")
  def refreshtest_click(self, **event_args):
    self.main_data_display()
    print(self.get_selected_runners())

