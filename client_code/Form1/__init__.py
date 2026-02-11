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

    self.text_boxes = []

    self.drop_down_1.items = [("Search",0),("PR",1),("Plot",2),("Average Times",3),("Optimal Varisty Lineup",4)]



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
    selected_runners = [checkmark_runner.text for checkmark_runner in self.runner_checkbox if checkmark_runner.checked]
    selected_lengths = [checkmark_length.text for checkmark_length in self.length_checkbox if checkmark_length.checked]
    selected_grades = [checkmark_grade.text for checkmark_grade in self.grade_checkbox if checkmark_grade.checked]
    self.repeating_panel_1.items = anvil.server.call("pr_display",selected_runners,selected_lengths,selected_grades)

  def graphing_module_display(self):
    selected_runners = [checkmark_runner.text for checkmark_runner in self.runner_checkbox if checkmark_runner.checked]
    selected_grades = [checkmark_grade.text for checkmark_grade in self.grade_checkbox if checkmark_grade.checked]
    selected_lengths = [checkmark_length.text for checkmark_length in self.length_checkbox if checkmark_length.checked]
    self.data_grid_1.visible = False
    self.plot_1.figure = anvil.server.call('graphing_module',selected_runners,selected_grades,selected_lengths)
    
  def optimal_varisty_team_display(self):
    selected_runners = [checkmark_runner.text for checkmark_runner in self.runner_checkbox]
    selected_races = [checkmark_race.text for checkmark_race in self.race_checkbox]
    
    list_averaged_times = anvil.server.call('optimal_varisity_lineup',selected_runners,3,selected_races)
    for runner,averaged_time in list_averaged_times:
      test1 = f"{runner} ran an average of {averaged_time}, across {race_amount} races"
      text_display_made = TextBox(text = test1)
      text_display_made.enabled = False
      self.text_boxes.append(text_display_made)
      self.text_display_column.add_component(text_display_made)

    
  @handle("import_csv_to_datattable", "click")
  def import_csv_to_datattable_click(self, **event_args):
    anvil.server.call('import_csf_to_table')

  @handle("refreshtest", "click")
  def refreshtest_click(self, **event_args):
    for text_display_made in self.text_boxes:
      text_display_made.remove_from_parent()
    self.text_boxes = []
    selected_value = self.drop_down_1.selected_value
    if selected_value == 0:
      self.main_data_display()
    elif selected_value == 1:
      self.pr_screen_display()
    elif selected_value == 2:
      self.graphing_module_display()
    elif selected_value == 3:
      self.average_time_display()
    elif selected_value == 4:
      self.optimal_varisty_team_display()

  def average_time_display(self):
    latest_races_to_check = int(self.text_input_box.text)
    if isinstance(latest_races_to_check,int) is False:
      self.text_display_1.text = "Please input only digits"
      return
    un_selected_races = [checkmark_race.text for checkmark_race in self.race_checkbox if checkmark_race.checked is False]
    selected_runners = [checkmark_runner.text for checkmark_runner in self.runner_checkbox if checkmark_runner.checked]
    if len(selected_runners) == 0:
      selected_runners = [checkmark_runner.text for checkmark_runner in self.runner_checkbox if checkmark_runner.checked is False]
    list_averaged_times,race_amount= anvil.server.call("average_time",selected_runners,latest_races_to_check,un_selected_races)

    for runner,averaged_time in list_averaged_times:
      test1 = f"{runner} ran an average of {averaged_time}, across {race_amount} races"
      text_display_made = TextBox(text = test1)
      text_display_made.enabled = False
      self.text_boxes.append(text_display_made)
      self.text_display_column.add_component(text_display_made)

    
      
      
    ##############################UI IS UNDER HERE###################################3


  def all_picker_on(self):
    self.flow_panel_grade.visible = True
    self.flow_panel_races.visible = True
    self.flow_panel_runner.visible = True
    self.flow_length.visible = True
    self.sorting_picker.visible = False

  def hide_all_display(self):
    self.data_grid_1.visible = False
    self.plot_1.visible = False
    self.text_display_column.visible = False

    
  @handle("sorting_picker", "change")
  def sorting_picker_change(self, **event_args):
    self.main_data_display()

  @handle("drop_down_1", "change")
  def drop_down_1_change(self, **event_args):
    selected_text = self.drop_down_1.selected_value
    self.all_picker_on()
    self.hide_all_display()
    self.text_display_1.text = ('')
    if selected_text == 0:
      self.sorting_picker.visible = True
      self.data_grid_1.visible = True
    elif selected_text == 1:
      self.flow_panel_races.visible = False
      self.data_grid_1.visible = True
    elif selected_text == 2:
      self.plot_1.visible = True
      self.flow_panel_races.visible = False
    elif selected_text == 3:
      self.text_input_box.text = 0
      self.flow_panel_grade.visible = False
      self.text_display_column.visible = True
      self.text_display_1.text = ("Please input how many latest races you want to check as a number, put 0 to average all.\nSelect what runners you'd like to check, what races to exclude, and the length of races")
    elif selected_text == 4:
      self.flow_panel_grade.visible = False
      self.flow_panel_races.visible = False
      self.flow_panel_runner.visible = False
      self.flow_length.visible = False
      self.sorting_picker.visible = False
      self.text_display_column.visible = True
