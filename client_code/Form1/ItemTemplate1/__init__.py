from ._anvil_designer import ItemTemplate1Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class ItemTemplate1(ItemTemplate1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
  def refresh_data_bindings(self, **event_args):
    """Called automatically when the RepeatingPanel sets self.item"""
    if self.item:  # ensures item exists
      self.label_runner.text = self.item['Runner']
      self.label_race.text = self.item['Race']
      self.label_placement.text = self.item['Placement']
      self.label_grade.text = self.item['Grade']
      self.label_time.text = self.item['Time']
      self.label_avrsplits.text = self.item['Average Splits']
      self.label_date.text = self.item['Date']
      self.label_length.text = self.item['Length']
    # Any code you write here will run before the form opens.

