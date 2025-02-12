import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build

def csv_to_google_sheets(csv_file_path, credentials_path, spreadsheet_title):
    # Read the CSV file
    df = pd.read_csv(csv_file_path)
    data = [df.columns.tolist()] + df.values.tolist()

    # Setup Google Sheets API credentials
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
    credentials = service_account.Credentials.from_service_account_file(credentials_path, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=credentials)

    # Create a new Google Sheets spreadsheet
    spreadsheet = {
        'properties': {
            'title': spreadsheet_title
        }
    }
    spreadsheet = service.spreadsheets().create(body=spreadsheet, fields='spreadsheetId').execute()
    spreadsheet_id = spreadsheet.get('spreadsheetId')
    print(f'Spreadsheet ID: {spreadsheet_id}')

    # Prepare data for Google Sheets
    body = {
        'values': data
    }

    # Upload data to the new spreadsheet
    result = service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range='Sheet1!A1',
        valueInputOption='RAW',
        body=body
    ).execute()

    print('Data successfully uploaded to Google Sheets')
    return spreadsheet_id

def main():
    csv_file_path = '/home/bilu/data_analisys_project/youtube_tutorial/scraped_quotes.csv'  # Update this path
    credentials_path = '/home/bilu/data_analisys_project/youtube_tutorial/credentials.json'  # Update this path
    spreadsheet_title = 'Scraped Quotes from Website'

    spreadsheet_id = csv_to_google_sheets(csv_file_path, credentials_path, spreadsheet_title)
    print(f'Google Sheets URL: https://docs.google.com/spreadsheets/d/{spreadsheet_id}')

if __name__ == "__main__":
    main()
