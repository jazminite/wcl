# Files
from __future__ import division
import secrets, lookup
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

def get_effective(reports, table, encounters, abilities, expression, sheet_info):
  for report in reports:
    reportId = str(report['id'], 'utf-8')
    print(report['date'], report['title'])
    for encounter in encounters:
      for ability in abilities:
        table_url = 'https://classic.warcraftlogs.com/v1/report/tables/%s/%s?end=36000000&abilityid=%s&filter=%s&api_key=%s' % (table, reportId, ability, expression, secrets.warcraft_logs_api_key)
        # print(table_url)
        r = requests.get(table_url)
        r_json = r.json()
        total_time = r_json['totalTime']
        for player in r_json['entries']:
          try:
            no_casts = player['total']
            uptime = player['uptime']
          except:
            # print('No uptime for ' + player['name'] + ' - ' + ability)
            uptime = 0

          ability_name = lookup.thisdict[ability] + '-Eff'
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
            lookup.thisdict[encounter],
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
  expression = 'type%3D%22cast%22%20AND%20ability.id%3D11597%20AND%20NOT%20IN%20RANGE%20FROM%20type%3D%22applydebuffstack%22%20AND%20ability.id%3D11597%20AND%20stack%3D5%20TO%20type%3D%22removedebuff%22%20AND%20ability.id%3D11597%20GROUP%20BY%20target%20ON%20target%20END'
  cast_info = get_effective(reports, 'casts', encounters, abilities, expression, start_info)
  print('Cast info retrieved')

  wks = wb.worksheet('warrior')
  wks.append_rows(cast_info, 'USER_ENTERED')
  print('Worksheet updated')

if __name__ == '__main__':
  main()
