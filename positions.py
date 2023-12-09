async def fetch_and_update_positions(api_token, account_id, positions_collection):
    # Use a single MetaApi instance for the application
    api = MetaApi(api_token)
    print("MetaApi instance created.")
    # Initialize connection, terminalState, and fetched_positions variables before the try block
    connection = None
    terminalState = None
    fetched_positions = []  # Default empty list in case of exception
    try:
        # Fetch account and use async with to manage the connection lifecycle
        account = await api.metatrader_account_api.get_account(account_id)
        connection = account.get_streaming_connection()
        await connection.connect()
        await connection.wait_synchronized()
        # Access local copy of terminal state
        terminalState = connection.terminal_state
        # Access positions from the terminal state if available
        if terminalState:
            fetched_positions = terminalState.positions
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Explicitly call garbage collector after the operation
        import gc
        gc.collect()
    print("Account and positions fetched.")

    # Store positions in Cosmos DB and create a list of fetched position ids
    fetched_position_ids = []
    for position in fetched_positions:
        positions_collection.update_one({'id': position['id']}, {"$set": position}, upsert=True)
        fetched_position_ids.append(position['id'])
    print(f"{len(fetched_positions)} positions updated or inserted in Cosmos DB.")

    # Fetch all positions from the database
    db_positions = positions_collection.find()

    # Remove positions from the database that are not in the fetched positions
    for db_position in db_positions:
        if db_position['id'] not in fetched_position_ids:
            positions_collection.delete_one({'id': db_position['id']})
    print("Positions not in the fetched data have been removed from the database.")