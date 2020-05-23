# Warcraft Log Scripts

These scripts are used to pull information from classic.warcraftlogs.com via their API.

- Rename `secrets.py.example` to `secrets.py` and fill in the relevant info

## Google Sheets Python API

- Create a Project at https://console.developers.google.com/cloud-resource-manager
- Add the Google Sheets API
- Add the Google Drive API
- Create Credentials
- Put the JSON file in the project directory
- Add the JSON file name to .gitignore
- Add the name of the JSON file to `secrets.py`
- Create a Google Sheet
- Share the Google Sheet with the `client_email` listed in the JSON file
- `pip install --upgrade google-api-python-client oauth2client`
- `pip install gspread`
