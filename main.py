# Files
from __future__ import division
import secrets
from sheets import update_sheet
from library import get_players

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
wks = wb.worksheet('parses')

def get_parses(players, table):
  for player in players:
    print(player)
    metric = 'dps'
    spec = 'dps'
    r = requests.get('https://classic.warcraftlogs.com/v1/parses/character/%s/Faerlina/US?api_key=%s&timeframe=historical&metric=%s' % (player, secrets.warcraft_logs_api_key, metric))
    char_parse = r.json()

    try:
      spec = char_parse[0]['spec']
    except:
      print('Error getting spec for ' + player)
      print(char_parse)

    if spec == 'Healer':
      metric = 'hps'
      r = requests.get('https://classic.warcraftlogs.com/v1/parses/character/%s/Faerlina/US?api_key=%s&timeframe=historical&metric=%s' % (player, secrets.warcraft_logs_api_key, metric))
      char_parse = r.json()

    for p in char_parse:
      if p['total'] > 0:
        new_row = [
          dt.datetime.fromtimestamp(p['startTime'] / 1000.0).strftime("%m/%d/%Y"), # date
          p['characterName'].encode('utf-8'), # player
          p['class'].encode('utf-8'), # class
          p['spec'].encode('utf-8'), # spec
          p['encounterName'].encode('utf-8'), # boss
          p['percentile'], # percentile
          p['total'] # dps / hps
        ]
        # print(new_row)
        table.append(new_row)

    time.sleep(7)

  return table

def main():
  players = get_players(secrets.report_ids)
  parses = get_parses(players, [])
  print('Table created')
  update_sheet(wks, parses)
  print('Worksheet updated')

if __name__ == '__main__':
  main()
