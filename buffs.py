# Files
from __future__ import division
import secrets
from library import get_reports, get_table

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

def get_buffs(reports, buff_ids):
  buffs = []
  for report in reports:
    for ability in buff_ids:
      r_json = get_table(report, 'buffs', ability)
      for player in r_json['auras']:
        new_row = [
          report['date'],
          str(report['id'], 'utf-8'),
          str(report['title'], 'utf-8'),
          player['name'],
          player['id'],
          ability,
          secrets.thisdict[ability]
        ]
        # print(new_row)
        buffs.append(new_row)

  return buffs

def main():
  reports = get_reports(secrets.raid_id, secrets.c_date)
  print('Reports retrieved')
  buffs = get_buffs(reports, secrets.buff_ids)
  print('Buffs retrieved')
  wks = wb.worksheet('buffs')
  wks.append_rows(buffs, 'USER_ENTERED')
  print('Worksheet updated')

if __name__ == '__main__':
  main()
