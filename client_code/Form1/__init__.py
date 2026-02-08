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
    self.race_checkbox = []
    self.grade_checkbox = []
    total_runner,total_races,total_grades = anvil.server.call('one_of_item')  
    checkmark_runner = CheckBox(text='All Runners',checked=True)
    self.flow_panel_runner.add_component(checkmark_runner)

    for runner in total_runner:
      checkmark_runner = CheckBox(text=runner,checked=False)
      self.flow_panel_runner.add_component(checkmark_runner)
      self.runner_checkbox.append(checkmark_runner)
    for race in total_races:
      checkmark_race = CheckBox(text=race,checked=False)
      self.flow_panel_races.add_component(checkmark_race)
      self.race_checkbox.append(checkmark_race)
    for grade in total_grades:
      checkmark_grade = CheckBox(text=grade,checked=False)
      self.flow_panel_grade.add_component(checkmark_grade)
      self.grade_checkbox.append(checkmark_grade)



    self.sorting_picker.items = [("Name","Runner"),("Time","time_seconds"),("Date","Date_dt")]
    # Any code you write here will run before the form opens.




  def main_data_display(self):
    selected_runners = [checkmark_runner.text for checkmark_runner in self.runner_checkbox if checkmark_runner.checked]
    selected_races = [checkmark_race.text for checkmark_race in self.race_checkbox if checkmark_race.checked]
    selected_grades = [checkmark_grade.text for checkmark_grade in self.grade_checkbox if checkmark_grade.checked]
    sort_by = self.sorting_picker.selected_value
    filtered_df = anvil.server.call('filter',sort_by,selected_runners,selected_races,selected_grades)
    self.repeating_panel_1.items = filtered_df


  @handle("import_csv_to_datattable", "click")
  def import_csv_to_datattable_click(self, **event_args):
    anvil.server.call('import_csf_to_table')

  @handle("refreshtest", "click")
  def refreshtest_click(self, **event_args):
    self.main_data_display()

  @handle("sorting_picker", "change")
  def sorting_picker_change(self, **event_args):
    self.

