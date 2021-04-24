# Files
from __future__ import division
import secrets, lookup
from sheets import update_sheet
from library import get_all_reports, get_table, get_friendlies

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

def get_raid_info(reports):
  raid_info = []
  for report in reports:
    players = get_friendlies(report)
    for player in players:
      zone = str(report['zone'])
      new_row = [
        report['date'],
        str(report['id'], 'utf-8'),
        str(report['title'], 'utf-8'),
        player['id'],
        player['name'],
        zone,
        lookup.thisdict[zone]
      ]
      # print(new_row)
      raid_info.append(new_row)

  return raid_info

def main():
  reports = get_all_reports(secrets.p_date)
  print('Reports retrieved')
  raid_info = get_raid_info(reports)
  print('Raid info retrieved')
  wks = wb.worksheet('promo')
  wks.append_rows(raid_info, 'USER_ENTERED')
  print('Worksheet updated')

if __name__ == '__main__':
  main()
