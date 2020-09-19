# Files
from __future__ import division
import secrets
from sheets import update_sheet
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
wks = wb.worksheet('add_damage')

def get_damage(reports, ability):
  damage = []
  for report in reports:
    r_json = get_table(report, 'damage-done', ability)
    for player in r_json['entries']:
      new_row = [
        report['date'],
        str(report['id'], 'utf-8'),
        str(report['title'], 'utf-8'),
        player['name'],
        player['id'],
        player['total'],
        ability
      ]
      # print(new_row)
      damage.append(new_row)

  return damage

def main():
  reports = get_reports(secrets.raid_id, secrets.c_date)
  print('Reports retrieved')
  damage = get_damage(reports, '13241') # Sapper charge
  print('Damage retrieved')
  update_sheet(wks, damage)
  print('Worksheet updated')

if __name__ == '__main__':
  main()
