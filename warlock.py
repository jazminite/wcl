# Files
from __future__ import division
import secrets
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
  reports = get_reports(secrets.raid_id, secrets.c_date)
  print('Reports retrieved')
  # encounters = ['709', '710', '711', '712', '713', '714', '715', '716', '717', '0'] # AQ40
  encounters = ['1107', '1108', '1109', '1110', '1111', '1112', '1113', '1114', '1115', '1116', '1117', '1118', '1119', '1120', '1121', '0'] # Naxx
  abilities = ['11717', '17937', '11722', '11713', '11672', '11661', '25307', '704', '11719', '11708']
  cast_info = get_casts(reports, 'casts', encounters, abilities)
  print('Cast info retrieved')
  wks = wb.worksheet('warlock')
  wks.append_rows(cast_info, 'USER_ENTERED')
  print('Worksheet updated')

if __name__ == '__main__':
  main()
