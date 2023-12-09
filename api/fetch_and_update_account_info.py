from http.server import BaseHTTPRequestHandler
from metaapi_cloud_sdk import MetaApi
from pymongo import MongoClient
import os
import asyncio

# Create a single, reusable MongoClient instance
client = MongoClient(os.getenv('MONGODB_URI'))

class handler(BaseHTTPRequestHandler):

    async def fetch_and_update_account_info(self):
        print("Starting fetch_and_update_account_info")
        api_token = os.getenv('META_API_TOKEN')
        account_id = os.getenv('META_API_ACCOUNT_ID')
        db_name = os.getenv('DB_NAME')

        db = client[db_name]
        account_info_collection = db['account_info']

        api = MetaApi(api_token)
        connection = None
        terminalState = None
        account_info = None
        try:
            account = await api.metatrader_account_api.get_account(account_id)
            connection = account.get_streaming_connection()
            await connection.connect()
            await connection.wait_synchronized()
            terminalState = connection.terminal_state
            if terminalState:
                account_info = terminalState.account_information
        except Exception as e:
            print(f"An error occurred: {e}")

        if account_info:
            account_info_collection.update_one({'id': account_id}, {"$set": account_info}, upsert=True)

        print("Finished fetch_and_update_account_info")
        return {
            'statusCode': 200,
            'body': 'Account info updated successfully'
        }

    def do_GET(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(self.fetch_and_update_account_info())
        self.send_response(200)
        self.end_headers()
        self.wfile.write(str(result).encode())
        return