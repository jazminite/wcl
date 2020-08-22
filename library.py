# Files
from __future__ import division
import secrets
from sheets import update_sheet

# Libraries
import requests
import datetime as dt
import gspread
import time

def get_reports(zone, c_date):
  r = requests.get('https://classic.warcraftlogs.com/v1/reports/guild/Quintessential/Faerlina/US?api_key=%s' % (secrets.warcraft_logs_api_key))
  r_json = r.json()

  reports = []
  titles = []
  for report in r_json:
    if report['zone'] == zone:
      raid_date = dt.datetime.fromtimestamp(report['start'] / 1000.0)
      if raid_date > c_date:
        title = report['title'].encode('utf-8')
        if title not in titles:
          titles.append(title)
          new_row = {
              'id': report['id'].encode('utf-8'),
              'title': title,
              'date': raid_date.strftime("%m/%d/%Y")
          }
          reports.append(new_row)

  return reports

def get_all_reports(c_date):
  r = requests.get('https://classic.warcraftlogs.com/v1/reports/guild/Quintessential/Faerlina/US?api_key=%s' % (secrets.warcraft_logs_api_key))
  r_json = r.json()

  reports = []
  titles = []
  for report in r_json:
    raid_date = dt.datetime.fromtimestamp(report['start'] / 1000.0)
    if raid_date > c_date:
      title = report['title'].encode('utf-8')
      if title not in titles:
        titles.append(title)
        new_row = {
            'id': report['id'].encode('utf-8'),
            'title': title,
            'date': raid_date.strftime("%m/%d/%Y"),
            'zone': report['zone'],
        }
        reports.append(new_row)

  return reports

def get_table(report, table, ability):
  reportId = str(report['id'], 'utf-8')
  print(report['date'], report['title'])
  if ability:
    table_url = 'https://classic.warcraftlogs.com/v1/report/tables/%s/%s?end=36000000&by=source&abilityid=%s&api_key=%s' % (table, reportId, ability, secrets.warcraft_logs_api_key)
  else:
    table_url = 'https://classic.warcraftlogs.com/v1/report/tables/%s/%s?end=36000000&by=source&api_key=%s' % (table, reportId, secrets.warcraft_logs_api_key)
  print(table_url)
  r = requests.get(table_url)

  return r.json()

def get_players(reports):
  players = []
  for report in reports:
    report_id = str(report['id'],'utf-8')
    url = 'https://classic.warcraftlogs.com/v1/report/fights/%s?api_key=%s' % (report_id, secrets.warcraft_logs_api_key)
    print(url)
    r = requests.get(url)
    r_json = r.json()
    for player in r_json['exportedCharacters']:
      # new_row = [
      #   report_id,
      #   player['name']
      # ]
      # players.append(new_row)
      players.append(player['name'])

  return players

def get_player_rows(reports):
  players = []
  for report in reports:
    report_id = str(report['id'],'utf-8')
    url = 'https://classic.warcraftlogs.com/v1/report/fights/%s?api_key=%s' % (report_id, secrets.warcraft_logs_api_key)
    print(url)
    r = requests.get(url)
    r_json = r.json()
    for player in r_json['exportedCharacters']:
      new_row = [
        report_id,
        player['name']
      ]
      players.append(new_row)

  return players

def get_friendlies(report):
  friendlies = []
  url = 'https://classic.warcraftlogs.com/v1/report/fights/%s?api_key=%s' % (str(report['id'],'utf-8'), secrets.warcraft_logs_api_key)
  print(url)
  r = requests.get(url)
  r_json = r.json()
  for player in r_json['friendlies']:
    new_row = {
          'id': player['id'],
          'name': player['name'],
      }
    friendlies.append(new_row)

  return friendlies
