# Files
from __future__ import division
import secrets
from sheets import update_sheet
from library import get_players, get_reports

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

def get_parses(players, table):
  for player in players:
    print(player)
    spec = 'dps'
    if player in secrets.healers:
      spec = 'hps'
      print('Healer')
    request_url = 'https://classic.warcraftlogs.com/v1/parses/character/%s/Faerlina/US?api_key=%s&timeframe=historical&metric=%s' % (player, secrets.warcraft_logs_api_key, spec)
    r = requests.get(request_url)
    char_parse = r.json()

    for p in char_parse:
      if p['total'] > 0:
        raid_date = dt.datetime.fromtimestamp(p['startTime'] / 1000.0)
        if raid_date > secrets.c_date:
          new_row = [
            raid_date.strftime("%m/%d/%Y"), # date
            p['characterName'], # player
            p['class'], # class
            p['spec'], # spec
            p['encounterName'], # boss
            p['percentile'], # percentile
            p['total'] # dps / hps
          ]
          # print(new_row)
          table.append(new_row)

    time.sleep(3)

  return table

def main():
  wks = wb.worksheet('add_parse')
  parses = get_parses(secrets.team_players, [])
  print('Table created')
  update_sheet(wks, parses)
  print('Worksheet updated')

if __name__ == '__main__':
  main()
