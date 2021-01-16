# Files
from __future__ import division
import secrets
from sheets import update_sheet
from library import get_reports, get_casts_type

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

def get_debuffs(reports, table, encounters, abilities, sheet_info):
  for report in reports:
    reportId = str(report['id'], 'utf-8')
    print(report['date'], report['title'])
    for encounter in encounters:
      for ability in abilities:
        table_url = 'https://classic.warcraftlogs.com/v1/report/tables/%s/%s?end=36000000&by=target&abilityid=%s&encounter=%s&api_key=%s' % (table, reportId, ability, encounter, secrets.warcraft_logs_api_key)
        # print(table_url)
        r = requests.get(table_url)
        r_json = r.json()
        total_time = r_json['totalTime']
        for player in r_json['auras']:
          try:
            no_casts = player['totalUses']
            uptime = player['uptime']
          except:
            # print('No uptime for ' + player['name'] + ' - ' + ability)
            uptime = 0

          ability_name = secrets.thisdict[ability] + '-Eff'
          new_row = [
            report['date'],
            str(report['id'], 'utf-8'),
            str(report['title'], 'utf-8'),
            player['name'],
            no_casts,
            total_time,
            uptime,
            uptime / total_time,
            ability,
            encounter,
            secrets.thisdict[encounter],
            ability_name
          ]
          # print(new_row)
          sheet_info.append(new_row)
  return sheet_info

def main():
  reports = get_reports(secrets.raid_id, secrets.c_date)
  print('Reports retrieved')

  encounters = ['-3']
  abilities = ['11597', '12328', '24427', '25891']
  start_info = get_casts_type(reports, 'casts', encounters, abilities, 'Warrior')
  abilities = ['11597']
  cast_info = get_debuffs(reports, 'debuffs', encounters, abilities, start_info)
  print('Cast info retrieved')

  wks = wb.worksheet('warrior')
  wks.append_rows(cast_info, 'USER_ENTERED')
  print('Worksheet updated')

if __name__ == '__main__':
  main()
