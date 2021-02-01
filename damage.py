# Files
from __future__ import division
import secrets, lookup
from library import get_reports, get_encounter

# Libraries
import requests
import datetime as dt
import gspread
import time

# Google Sheets
from oauth2client.service_account import ServiceAccountCredentials
from apiclient.discovery import build
from httplib2 import Http

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name(secrets.google_json_file, scope)
gc = gspread.authorize(credentials)
service = build('sheets', 'v4', http=credentials.authorize(Http()))

wb = gc.open_by_key(secrets.google_sheet_id)

def get_damage(reports, encounters):
  damage = []
  for report in reports:
    for encounter in encounters:
      r_json = get_encounter(report, 'damage-done', encounter)
      # totalTime = total combat time in milliseconds
      combat_time = r_json['totalTime'] / 1000
      for player in r_json['entries']:
        # DPS: player.total / (totalTime / 1000)
        dps = player['total'] / combat_time
        new_row = [
          report['date'],
          str(report['id'], 'utf-8'),
          str(report['title'], 'utf-8'),
          player['name'],
          player['id'],
          player['total'],
          dps,
          encounter,
          lookup.thisdict[encounter]
        ]
        # print(new_row)
        damage.append(new_row)

  return damage

def main():
  reports = get_reports(secrets.raid_id, secrets.c_date)
  print('Reports retrieved')
  encounters = ['-3', '-2', '0']
  damage = get_damage(reports, encounters)
  print('Damage retrieved')
  wks = wb.worksheet('damage')
  wks.append_rows(damage, 'USER_ENTERED')
  print('Worksheet updated')

if __name__ == '__main__':
  main()
