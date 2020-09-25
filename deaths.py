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

def get_deaths(reports):
  death_table = []
  for report in reports:
    r_json = get_table(report, 'survivability', None)
    players = r_json['players']
    for player in players:
      fights = player['fights']
      for fight in fights:
        deaths = fight['deaths']
        for death in deaths:
          sources = death['damage']['sources']
          if len(sources) > 0:
            source = sources[0]['name']
            dmg_type = sources[0]['type']
            if dmg_type == 'Boss':
              kind = 'Boss'
            elif dmg_type == 'NPC':
              kind = 'Trash'
            else:
              kind = 'Friendly'
          else:
            source = 'Divine Intervention'
            kind = 'Friendly'
          new_row = [
              report['date'],
              str(report['id'], 'utf-8'),
              str(report['title'], 'utf-8'),
              player['name'],
              source,
              kind,
              1
          ]
          death_table.append(new_row)

  return death_table

def main():
  reports = get_reports(secrets.raid_id, secrets.c_date)
  print('Reports retrieved')
  deaths = get_deaths(reports)
  print('Deaths retrieved')
  wks = wb.worksheet('deaths')
  wks.append_rows(deaths, 'USER_ENTERED')
  print('Worksheet updated')

if __name__ == '__main__':
  main()
