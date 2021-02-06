# Files
from __future__ import division
import secrets
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

def main():
  reports = get_reports(secrets.raid_id, secrets.c_date)
  print('Reports retrieved')
  encounters = ['709', '710', '711', '712', '713', '714', '715', '716', '717', '-3']
  abilities = ['13877', '13750', '25891', '1769', '24532', '9512', '28866']
  cast_info = get_casts_type(reports, 'casts', encounters, abilities, 'Rogue')
  print('Cast info retrieved')
  wks = wb.worksheet('rogue')
  wks.append_rows(cast_info, 'USER_ENTERED')
  print('Worksheet updated')

if __name__ == '__main__':
  main()
