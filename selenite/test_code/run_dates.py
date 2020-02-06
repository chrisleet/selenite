import subprocess

def run_dates():
  dates = ["180601"]
  for date in dates:
    subprocess.call(["python3", "Scripts/telluric_modelling.py", date, "-v", \
                     "-db", "date_dbs", "-date_mode"])

if __name__ == "__main__":
  run_dates()
