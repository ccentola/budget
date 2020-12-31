import mintapi
import pandas as pd
import gspread
from df2gspread import df2gspread as d2g
from oauth2client.service_account import ServiceAccountCredentials
from config import username, password

mint = mintapi.Mint(
    username,
    password,
    mfa_method='sms', # will need to try and automate
    headless=False,
    mfa_input_callback=None,
    session_path=None,
    imap_account=None,
    imap_password=None,
    imap_server=None,
    imap_folder='INBOX',
    wait_for_sync=False,
    wait_for_sync_timeout=300
)

# get transactions
transactions=mint.get_transactions()

# drop unused columns
transactions=transactions.drop(['labels','notes'],axis=1)

transactions.loc[(transactions.transaction_type == 'debit'),'budget_category'] = 'Expense'
transactions.loc[(transactions.transaction_type == 'credit'),'budget_category'] = 'Income'

# https://docs.google.com/spreadsheets/d/1tIKaMNdMT3M2mz2ysHAUsvNZS2R_j8dXkCvF9cPOiiw/edit#gid=901716447

# write to google sheets
scope=['https://spreadsheets.google.com/feeds']
creds=ServiceAccountCredentials.from_json_keyfile_name('credentials_mint.json',scope)
client=gspread.authorize(creds)
spreadsheet_key='1tIKaMNdMT3M2mz2ysHAUsvNZS2R_j8dXkCvF9cPOiiw'
d2g.upload(transactions,spreadsheet_key,'transactions_mint',credentials=creds,row_names=True)

# close session
mint.close()