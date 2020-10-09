# Warcraft Log Scripts

These scripts are used to pull information from classic.warcraftlogs.com via their API.

## Setup
### Secrets file

- Rename `secrets.py.example` to `secrets.py` and fill in the relevant info

### Google Sheets Python API

- Create a Project at https://console.developers.google.com/cloud-resource-manager
- Add the Google Sheets API
- Add the Google Drive API
- Create Credentials
- Put the JSON file in the project directory
- Add the JSON file name to .gitignore
- Add the name of the JSON file to `secrets.py`
- Create a Google spreadsheet
- Share the Google spreadsheet with the `client_email` listed in the JSON file
- `pip install --upgrade google-api-python-client oauth2client`
- `pip install gspread`

### Google spreadsheet

- Set up sheets similar to the example file 

## Usage

### Parses

1. `secrets.py`: Update the date
2. `players`: Remove data from columns A to C
2. `python main.py`: Get a list of players from recent reports
3. `player-export`: Export the guild roster from the game
4. `players`: Copy new players from column B to F, Filter out people not in the guild
5. `current-players`: Update current players with the teams spreadsheet
6. `players`: Update missing player specs
7. `secrets.py`: Update healers array
8. `add_parse`: Clear sheet
9. `python parses.py`: Run the parse script
10. `parses`: Add new data from `add_parse`
11. `players`: Filter / highlight based on the Parse sheet column
12. `Parses over`: Paste Player column from `players`, drag formulas, sort, increase date field, remove people with zero parse

### Other reports

For other reports, run the scripts:

- `python buffs.py`: Buffs
- `python caster.py`: Caster
- `python damage.py`: Damage
- `python deaths.py`: Deaths
- `python paladin.py`: Paladins
- `python priest.py`: Priests
- `python rogue.py`: Rogues
- `python warlock.py`: Warlocks
- `python warrior.py`: Warriors

## Post

- Raid time comparisons
- Death Report
- World Buff Report
- Class and Role reports
- Raid Analysis sheet link

## TODO

- Warlock Analysis (see pins in #warlock)
