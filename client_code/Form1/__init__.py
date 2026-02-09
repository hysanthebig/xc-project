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
    self.data_grid_1.role = 'wide'
   
#############################################Filter UI##############################################
    self.runner_checkbox = []
    self.race_checkbox = []
    self.grade_checkbox = []
    total_runner,total_races,total_grades,total_lengths = anvil.server.call('one_of_item')  
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
  ###############################PR UI###################################
    self.pr_length_checkbox = []
    self.pr_grade_checkbox = []
    for grade in total_grades:
      checkmark_pr_grade = CheckBox(text=grade,checked=False)
      self.flow_pr_grade.add_component(checkmark_pr_grade)
      self.pr_grade_checkbox.append(checkmark_pr_grade)
    for length in total_lengths:
      checkmark_pr_length = CheckBox(text=length,checked=False)
      self.flow_pr_length.add_component(checkmark_pr_length)
      self.pr_length_checkbox.append(checkmark_pr_length)

    self.sorting_picker.items = [("Name","Runner"),("Time","time_seconds"),("Date","Date_dt")]

    #####sidescroll

    # Any code you write here will run before the form opens.




  def main_data_display(self):
    selected_runners = [checkmark_runner.text for checkmark_runner in self.runner_checkbox if checkmark_runner.checked]
    selected_races = [checkmark_race.text for checkmark_race in self.race_checkbox if checkmark_race.checked]
    selected_grades = [checkmark_grade.text for checkmark_grade in self.grade_checkbox if checkmark_grade.checked]
    sort_by = self.sorting_picker.selected_value
    filtered_df = anvil.server.call('filter',sort_by,selected_runners,selected_races,selected_grades)
    self.repeating_panel_1.items = filtered_df


  def pr_screen_display(self):
    selected_lengths = [checkmark_pr_length.text for checkmark_pr_length in self.pr_length_checkbox if checkmark_pr_length.checked]
    selected_grades = [checkmark_pr_grade.text for checkmark_pr_grade in self.pr_grade_checkbox if checkmark_pr_grade.checked]
    self.repeating_panel_1.items = anvil.server.call("pr_display",selected_lengths,selected_grades)

  @handle("import_csv_to_datattable", "click")
  def import_csv_to_datattable_click(self, **event_args):
    anvil.server.call('import_csf_to_table')

  @handle("refreshtest", "click")
  def refreshtest_click(self, **event_args):
    if self.column_panel_2.visible is True:
      self.main_data_display()
    elif self.column_panel_3.visible is True:
      self.pr_screen_display()

  @handle("sorting_picker", "change")
  def sorting_picker_change(self, **event_args):
    self.main_data_display()

  @handle("select_pr", "clicked")
  def select_pr_clicked(self, **event_args):
    self.column_panel_2.visible = False
    self.column_panel_3.visible = True
    self.sorting_picker.visible = False


  @handle("select_search", "clicked")
  def select_search_clicked(self, **event_args):
    self.column_panel_2.visible = True
    self.column_panel_3.visible = False
    self.sorting_picker.visible = True