import anvil.files
from anvil.files import data_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

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
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from datetime import datetime

# ================= CONFIG =================
URL = "https://files.finishedresults.com/Track2026/Meets/13770-Colony-vs-Alta-Loma.html"
CSV_PATH = "/storage/emulated/0/pythondata/track_data.csv"
SCHOOL_NAME = "colony"  # case-insensitive
SPORT = "Track"
MEET_NAME = "Colony Vs Alta Loma"
MEET_DATE = "3/26/2026"
# ==========================================


pd.set_option('display.max_columns',None)
pd.set_option('display.width',None)
pd.set_option('display.max_rows',None)


# Helper: convert mm:ss string to total seconds
def time_to_seconds(time_str):
  minutes, seconds = time_str.split(":")
  return int(minutes) * 60 + float(seconds)

# Helper: average split per distance in minutes:seconds
def avg_split(time_str, distance_meters):
  total_seconds = time_to_seconds(time_str)
  avg_sec = total_seconds / (distance_meters / 1609.34)  # convert meters to miles if needed
  minutes = int(avg_sec // 60)
  seconds = int(round(avg_sec % 60))
  return f"{minutes}:{seconds:02d}"

# ====== Parsing HTML ======
def get_html(url):
  r = requests.get(url)
  r.raise_for_status()
  return r.text

def parse_html(html):
  soup = BeautifulSoup(html, "html.parser")
  text = soup.get_text("\n")
  lines = [line.strip() for line in text.splitlines() if line.strip()]

  records = []
  current_event = None
  current_race_type = None
  current_distance = None
  current_event_number = None

  # Event header regex
  event_regex = re.compile(
    r"Event\s+(\d+)\s+(.*?)\s+(Varsity|FS|Frosh/Soph|[A-Za-z]+)?$",
    re.IGNORECASE
  )

  # Runner regex
  runner_regex = re.compile(
    r"(?P<place>\d+)\s+"
    r"(?P<name>[A-Z][a-zA-Z ,\-\(\)']+?)\s+"
    r"(?P<grade>\d{1,2})\s+"
    r"(?P<team>.+?)\s+"
    r"(?P<time>\d+:\d+\.\d+)"
  )

  for line in lines:
    # Check for event header
    ev = event_regex.search(line)
    if ev:
      current_event_number = ev.group(1)
      event_name_dist = ev.group(2).strip()
      current_race_type = ev.group(3).strip() if ev.group(3) else "Unknown"
      # Extract distance (first number + Meter)
      dist_match = re.search(r"(\d+[x]?\d*\s?Meter)", event_name_dist)
      current_distance = dist_match.group(1) if dist_match else "Unknown"
      current_event = f"{current_event_number}_{current_distance}_{current_race_type}"
      continue

      # Check for runner row
    m = runner_regex.match(line)
    if m and current_event:
      records.append({
        "Placement": int(m.group("place")),
        "Runner": m.group("name").strip(),
        "Grade": int(m.group("grade")),
        "Team": m.group("team").strip(),
        "Time": m.group("time"),
        "EventID": current_event,
        "RaceType": current_race_type,
        "Length": current_distance
      })

  df = pd.DataFrame(records)
  def flip_name(name):
    if "," in name:
      last, first = name.split(",", 1)
      return f"{first.strip()} {last.strip()}"
    return name

  df['Runner'] = df['Runner'].apply(flip_name)



  return df



# ====== Placement / School Filter ======
def compute_school_placement(df_full, school_name):
    totals = df_full.groupby("EventID")["Placement"].max()
    df_school = df_full[df_full["Team"].str.contains(school_name, case=False, na=False)].copy()
    df_school["Placement"] = df_school.apply(
        lambda r: f"{r['Placement']}/{totals[r['EventID']]}",
        axis=1
    )
    return df_school

# ====== Reformat Columns for CSV ======
def format_for_csv(df_school, race_distance_meters=1600):
    df = df_school.copy()
    df["Race"] = MEET_NAME
    df["Date"] = MEET_DATE
    df["Sport"] = SPORT
    df["Avr splits"] = df["Time"].apply(lambda t: avg_split(t, race_distance_meters))
    df["Date_dt"] = pd.to_datetime(df["Date"])
    df["time_seconds"] = df["Time"].apply(time_to_seconds)

    # Reorder columns
    df = df[["Runner", "Race", "Placement", "Grade", "Time",
             "Avr splits", "Date", "Length", "RaceType", "Sport",
             "Date_dt", "time_seconds"]]

    return df


# ====== Main Pipeline ======
def main():
    html = get_html(URL)
    df_full = parse_html(html)
    df_school = compute_school_placement(df_full, SCHOOL_NAME)
    df_full = format_for_csv(df_school)
    df_final = df_full[df_full["Length"].str.contains("800|1600|3200", na=False)]

    print(df_final)
    

    confirm = input("Save results? (y/n): ").lower()
    if confirm == "y":
        try:
            df_target = pd.read_csv(CSV_PATH)
            df_target = pd.concat([df_target, df_final], ignore_index=True)
        except FileNotFoundError:
            df_target = df_final
        df_target.to_csv(CSV_PATH, index=False)
        print("Saved.")
    else:
        print("Aborted.")

