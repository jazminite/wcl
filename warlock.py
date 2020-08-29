# Files
from __future__ import division
import secrets
from sheets import update_sheet
from library import get_reports

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

def get_casts(reports, table, abilities, encounter):
  casts = []
  for report in reports:
    reportId = str(report['id'], 'utf-8')
    print(report['date'], report['title'])
    for ability in abilities:
      table_url = 'https://classic.warcraftlogs.com/v1/report/tables/%s/%s?end=36000000&by=source&abilityid=%s&encounter=%s&api_key=%s' % (table, reportId, ability, encounter, secrets.warcraft_logs_api_key)
      # print(table_url)
      r = requests.get(table_url)
      r_json = r.json()
      total_time = r_json['totalTime']
      for player in r_json['entries']:
        try:
          no_casts = player['total']
          uptime = player['uptime']
        except:
          print('No uptime for ' + player['name'] + ' - ' + ability)
          uptime = 0

        new_row = [
          report['date'],
          str(report['id'], 'utf-8'),
          str(report['title'], 'utf-8'),
          player['name'],
          no_casts,
          total_time,
          uptime,
          uptime / total_time,
          ability
        ]
        # print(new_row)
        casts.append(new_row)

  return casts

def main():
  wks = wb.worksheet('add_warlock')
  reports = get_reports(secrets.raid_id, secrets.c_date)
  print('Reports retrieved')
  abilities = ['11717', '17937', '11722', '11713', '11672', '11661', '25307']
  cast_info = get_casts(reports, 'casts', abilities, '-2')
  print('Cast info retrieved')
  update_sheet(wks, cast_info)
  print('Worksheet updated')

if __name__ == '__main__':
  main()


