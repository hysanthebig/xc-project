from ._anvil_designer import RowTemplate2Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class RowTemplate2(RowTemplate2Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    if hasattr(self, "item") and self.item:
      self.lbl_runner.text = str(self.item.get('Runner', ''))
      self.lbl_race.text = str(self.item.get('Race', ''))
      self.lbl_grade.text = str(self.item.get('Grade', ''))
      self.lbl_placement.text = str(self.item.get('Placement', ''))
      self.lbl_time.text = str(self.item.get('Time', ''))
      self.lbl_avr_splits.text = str(self.item.get('Avr_splits', ''))
      self.lbl_date.text = str(self.item.get('Date', ''))
      self.lbl_length.text = str(self.item.get('Length', ''))
      self.lbl_date_dt.text = str(self.item.get('Date_dt', ''))
      self.lbl_time_seconds.text = str(self.item.get('time_seconds', ''))

    # Any code you write here will run before the form opens.
