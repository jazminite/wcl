# Files
from __future__ import division
import secrets
from sheets import update_sheet
from library import get_player_rows, get_reports

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
  wks = wb.worksheet('players')
  reports = get_reports(secrets.raid_id, secrets.c_date)
  players = get_player_rows(reports)
  update_sheet(wks, players)

if __name__ == '__main__':
  main()
