import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import logging

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

def authenticate_google_sheets():
    try:
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
        client = gspread.authorize(creds)
        return client
    except Exception as e:
        logger.error(f"Error authenticating with Google Sheets API: {e}")
        st.error("Authentication error. Please check your credentials.")
        return None
def load_google_sheet(client, sheet_name):
    try:
        sheet = client.open(sheet_name).sheet1
        return sheet
    except gspread.SpreadsheetNotFound:
        logger.error(f"Google Sheet '{sheet_name}' not found.")
        st.error(f"Google Sheet '{sheet_name}' not found. Please check the name.")
        return None
st.title('Google Sheets Data Updater')
with st.sidebar:
    st.write('## Update Data')
    sheet_name = st.text_input('Google Sheet Name:')
    row = st.number_input('Row:', min_value=1, step=1)
    column = st.number_input('Column:', min_value=1, step=1)
    data_type = st.selectbox('Data Type:', ['Text', 'Numeric'])
    value = st.text_input('Value:')
    update_button = st.button('Update')
if update_button:
    client = authenticate_google_sheets()
    if client:
        sheet = load_google_sheet(client, sheet_name)
        if sheet:
            if 1 <= row <= sheet.row_count and 1 <= column <= sheet.col_count:
                try:
                    if data_type == 'Text':
                        sheet.update_cell(row, column, value)
                        st.success('Text data updated successfully!')
                    elif data_type == 'Numeric':
                        sheet.update_cell(row, column, float(value))
                        st.success('Numeric data updated successfully!')
                except Exception as e:
                    logger.error(f"Error updating data: {e}")
                    st.error(f"Error updating data: {e}")
            else:
                st.error("Row or column number out of range. Please provide valid values.")
