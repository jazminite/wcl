# Files
from __future__ import division
import secrets
from sheets import update_sheet
from library import get_reports, get_casts

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

def main():
  wks = wb.worksheet('add_paladin')
  reports = get_reports(secrets.raid_id, secrets.c_date)
  print('Reports retrieved')
  encounters = ['-3']
  abilities = ['10278', '4987', '10310']
  cast_info = get_casts(reports, 'casts', encounters, abilities)
  print('Cast info retrieved')
  # print(cast_info)
  update_sheet(wks, cast_info)
  print('Worksheet updated')

if __name__ == '__main__':
  main()
