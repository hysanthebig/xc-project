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
    self.length_checkbox = []
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
    for length in total_lengths:
      checkmark_length = CheckBox(text=length,checked=False)
      self.flow_length.add_component(checkmark_length)
      self.length_checkbox.append(checkmark_length)

    self.sorting_picker.items = [("Name","Runner"),("Time","time_seconds"),("Date","Date_dt")]

    #####sidescroll

    # Any code you write here will run before the form opens.
    
  

  def main_data_display(self):
    selected_runners = [checkmark_runner.text for checkmark_runner in self.runner_checkbox if checkmark_runner.checked]
    selected_races = [checkmark_race.text for checkmark_race in self.race_checkbox if checkmark_race.checked]
    selected_grades = [checkmark_grade.text for checkmark_grade in self.grade_checkbox if checkmark_grade.checked]
    selected_lengths = [checkmark_length.text for checkmark_length in self.length_checkbox if checkmark_length.checked]
    sort_by = self.sorting_picker.selected_value
    filtered_df = anvil.server.call('filter',sort_by,selected_runners,selected_races,selected_grades,selected_lengths)
    self.repeating_panel_1.items = filtered_df


  def pr_screen_display(self):
    selected_lengths = [checkmark_length.text for checkmark_length in self.length_checkbox if checkmark_length.checked]
    selected_grades = [checkmark_grade.text for checkmark_grade in self.pr_grade_checkbox if checkmark_grade.checked]
    self.repeating_panel_1.items = anvil.server.call("pr_display",selected_lengths,selected_grades)

  def graphing_module_display(self):
    selected_runners = [checkmark_runner.text for checkmark_runner in self.runner_checkbox if checkmark_runner.checked]
    selected_grades = [checkmark_grade.text for checkmark_grade in self.grade_checkbox if checkmark_grade.checked]
    selected_lengths = [checkmark_length.text for checkmark_length in self.length_checkbox if checkmark_length.checked]
    self.data_grid_1.visible = False
    self.plot_1.figure = anvil.server.call('graphing_module',selected_runners,selected_grades,selected_lengths)
    
    
  @handle("import_csv_to_datattable", "click")
  def import_csv_to_datattable_click(self, **event_args):
    anvil.server.call('import_csf_to_table')

  @handle("refreshtest", "click")
  def refreshtest_click(self, **event_args):
    if self.select_search.selected is True:
      self.main_data_display()
    elif self.select_pr.selected is True:
      self.pr_screen_display()
    elif self.select_plot.selected is True:
      self.graphing_module_display()


  def all_picker_on(self):
    self.flow_panel_grade.visible = True
    self.flow_panel_races.visible = True
    self.flow_panel_runner.visible = True
    self.flow_length.visible = True

    
  @handle("sorting_picker", "change")
  def sorting_picker_change(self, **event_args):
    self.main_data_display()

  @handle("select_pr", "clicked")
  def select_pr_clicked(self, **event_args):
    self.all_picker_on()
    self.flow_panel_races
    self.sorting_picker.visible = False


  @handle("select_search", "clicked")
  def select_search_clicked(self, **event_args):
    self.all_picker_on()
    self.sorting_picker.visible = True

  @handle("select_plot", "clicked")
  def select_plot_clicked(self, **event_args):
    self.all_picker_on()
    self.flow_panel_races.visible = False

