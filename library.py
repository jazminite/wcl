# Files
from __future__ import division
import secrets, lookup
from sheets import update_sheet

# Libraries
import requests
import datetime as dt
import gspread
import time

def get_reports(zone, c_date):
  r = requests.get('https://classic.warcraftlogs.com/v1/reports/guild/%s/%s/US?api_key=%s' % (secrets.guild, secrets.server, secrets.warcraft_logs_api_key))
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
  r = requests.get('https://classic.warcraftlogs.com/v1/reports/guild/%s/%s/US?api_key=%s' % (secrets.guild, secrets.server, secrets.warcraft_logs_api_key))
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
  print(report['date'], report['title'], reportId)
  if ability:
    table_url = 'https://classic.warcraftlogs.com/v1/report/tables/%s/%s?end=36000000&by=source&abilityid=%s&api_key=%s' % (table, reportId, ability, secrets.warcraft_logs_api_key)
  else:
    table_url = 'https://classic.warcraftlogs.com/v1/report/tables/%s/%s?end=36000000&by=source&api_key=%s' % (table, reportId, secrets.warcraft_logs_api_key)
  # print(table_url)
  r = requests.get(table_url)

  return r.json()

def get_encounter(report, table, encounter):
  reportId = str(report['id'], 'utf-8')
  print(report['date'], report['title'], reportId)
  table_url = 'https://classic.warcraftlogs.com/v1/report/tables/%s/%s?end=36000000&by=source&encounter=%s&api_key=%s' % (table, reportId, encounter, secrets.warcraft_logs_api_key)
  r = requests.get(table_url)
  return r.json()

def get_players(reports):
  players = []
  for report in reports:
    report_id = str(report['id'],'utf-8')
    url = 'https://classic.warcraftlogs.com/v1/report/fights/%s?api_key=%s' % (report_id, secrets.warcraft_logs_api_key)
    # print(url)
    r = requests.get(url)
    r_json = r.json()
    for player in r_json['exportedCharacters']:
      player = player['name']
      if player not in players:
        players.append(player)

  return players

def get_player_rows(reports):
  players = []
  for report in reports:
    report_id = str(report['id'],'utf-8')
    url = 'https://classic.warcraftlogs.com/v1/report/fights/%s?api_key=%s' % (report_id, secrets.warcraft_logs_api_key)
    # print(url)
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
  # print(url)
  r = requests.get(url)
  r_json = r.json()
  for player in r_json['friendlies']:
    new_row = {
          'id': player['id'],
          'name': player['name'],
      }
    friendlies.append(new_row)

  return friendlies

def get_casts(reports, table, encounters, abilities):
  casts = []
  for report in reports:
    reportId = str(report['id'], 'utf-8')
    print(report['date'], report['title'])
    for encounter in encounters:
      for ability in abilities:
        table_url = 'https://classic.warcraftlogs.com/v1/report/tables/%s/%s?end=36000000&by=source&abilityid=%s&encounter=%s&wipes=2&api_key=%s' % (table, reportId, ability, encounter, secrets.warcraft_logs_api_key)
        # print(ability)
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
            lookup.thisdict[ability]
          ]
          # print(new_row)
          casts.append(new_row)

  return casts

def get_casts_type(reports, table, encounters, abilities, clss):
  casts = []
  for report in reports:
    reportId = str(report['id'], 'utf-8')
    print(report['date'], report['title'])
    for encounter in encounters:
      for ability in abilities:
        table_url = 'https://classic.warcraftlogs.com/v1/report/tables/%s/%s?end=36000000&by=source&abilityid=%s&encounter=%s&api_key=%s' % (table, reportId, ability, encounter, secrets.warcraft_logs_api_key)
        print(table_url)
        r = requests.get(table_url)
        r_json = r.json()
        total_time = r_json['totalTime']
        for player in r_json['entries']:
          if player['type'] == clss:
            try:
              no_casts = player['total']
              uptime = player['uptime']
            except:
              # print('No uptime for ' + player['name'] + ' - ' + ability)
              uptime = 0

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
              lookup.thisdict[ability]
            ]
            # print(new_row)
            casts.append(new_row)

  return casts