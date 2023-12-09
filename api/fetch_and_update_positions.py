from http.server import BaseHTTPRequestHandler
from metaapi_cloud_sdk import MetaApi
from pymongo import MongoClient
import os
import asyncio

# Create a single, reusable MongoClient instance
client = MongoClient(os.getenv('MONGODB_URI'))

class handler(BaseHTTPRequestHandler):

    async def fetch_and_update_positions(self):
        print("Starting fetch_and_update_positions")
        api_token = os.getenv('META_API_TOKEN')
        account_id = os.getenv('META_API_ACCOUNT_ID')
        db_name = os.getenv('DB_NAME')

        db = client[db_name]
        positions_collection = db['positions']

        api = MetaApi(api_token)
        connection = None
        terminalState = None
        fetched_positions = []
        try:
            account = await api.metatrader_account_api.get_account(account_id)
            connection = account.get_streaming_connection()
            await connection.connect()
            await connection.wait_synchronized()
            terminalState = connection.terminal_state
            if terminalState:
                fetched_positions = terminalState.positions
        except Exception as e:
            print(f"An error occurred: {e}")

        fetched_position_ids = []
        for position in fetched_positions:
            positions_collection.update_one({'id': position['id']}, {"$set": position}, upsert=True)
            fetched_position_ids.append(position['id'])

        print(f"{len(fetched_positions)} positions updated or inserted into MongoDB.")

        db_positions = positions_collection.find()
        for db_position in db_positions:
            if db_position['id'] not in fetched_position_ids:
                positions_collection.delete_one({'id': db_position['id']})

        print("Finished fetch_and_update_positions")
        return {
            'statusCode': 200,
            'body': 'Positions updated successfully'
        }

    def do_GET(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(self.fetch_and_update_positions())
        self.send_response(200)
        self.end_headers()
        self.wfile.write(str(result).encode())
        return