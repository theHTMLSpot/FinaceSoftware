import os
from dotenv import load_dotenv
import plaid
from plaid.api import plaid_api
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.accounts_balance_get_request import AccountsBalanceGetRequest
from plaid.model.auth_get_request import AuthGetRequest

# Load environment variables from .env file
load_dotenv()

# Access API keys from environment variables
PLAID_CLIENT_ID = os.getenv('PLAID_CLIENT_ID')
PLAID_SECRET = os.getenv('PLAID_SECRET')
PLAID_ENV = os.getenv('PLAID_ENV')

# Initialize Plaid client
configuration = plaid.Configuration(
    host=plaid.Environment.Sandbox if PLAID_ENV == 'sandbox' else plaid.Environment.Development,
    api_key={
        'clientId': PLAID_CLIENT_ID,
        'secret': PLAID_SECRET,
    }
)
api_client = plaid.ApiClient(configuration)
client = plaid_api.PlaidApi(api_client)

def get_plaid_access_token(public_token):
    exchange_request = ItemPublicTokenExchangeRequest(public_token=public_token)
    exchange_response = client.item_public_token_exchange(exchange_request)
    return exchange_response['access_token']

def get_account_balance(access_token):
    balance_request = AccountsBalanceGetRequest(access_token=access_token)
    balance_response = client.accounts_balance_get(balance_request)
    return balance_response['accounts']

def get_auth_info(access_token):
    auth_request = AuthGetRequest(access_token=access_token)
    auth_response = client.auth_get(auth_request)
    return auth_response['accounts']

# Example usage
public_token = 'your_public_token'  # Obtain this from Plaid Link integration
access_token = get_plaid_access_token(public_token)
accounts = get_account_balance(access_token)
auth_info = get_auth_info(access_token)

print("Account Balances:")
for account in accounts:
    print(f"Account Name: {account['name']}")
    print(f"Available Balance: {account['balances']['available']}")
    print(f"Current Balance: {account['balances']['current']}")
    print(f"Balance Currency: {account['balances']['currency']}")
    print("")

print("Account Auth Information:")
for account in auth_info:
    print(f"Account Name: {account['name']}")
    print(f"Account Number: {account['account_id']}")
    print(f"Routing Number: {account['routing_numbers']['ach']}")
    print("")