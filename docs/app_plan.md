## Overview of systems

1. Data Fetching:
- Use MetaApi's RPC for one-time requests (e.g., account info, positions, orders). See ALL_rpcExample.py.
- Use MetaApi's Synchronization API for real-time state synchronization. See ALL_synchronizationExample.py.
- Use MetaApi's Streaming API for real-time updates (e.g., market data, account status). See ALL_streamingApi.rst.

2. Data Storage:
- Store fetched data in Atlas MongoDB, a scalable NoSQL database ideal for JSON-like documents.

3. Data Usage:
- Fetch stored data from MongoDB as needed. Create views or endpoints for specific data retrieval.

## Determine fetch method combination for each 'type'

    - type = ('account_information', 'positions', 'orders', 'deals', 'history_orders')
    - get the data to Atlas mongo with a sync method. (prevent storing dups)
    - additionally 'listen' for data changes real-time and note how often the data changes to make a determination on whether a basic sync on an interval will be sufficient or if we need to implement a more complex data store method.

4. Visualization:
- For each 'type', Use Panel HoloViz for interactive data visualization. It works well with PyData tools (pandas, numpy, matplotlib).


## 'positions' main.py

- The script starts by importing necessary libraries and modules for data manipulation, web server, and interaction with MetaApi and MongoDB.

- It loads environment variables from a .env file, which include MetaApi token, account id, MongoDB URI, and database name.

- It establishes a connection to MongoDB using the provided URI and database name, and creates a change stream to monitor changes in the 'positions' collection.

- It fetches all documents from the 'positions' collection in MongoDB and converts them into a pandas DataFrame.

- The DataFrame is then grouped by 'symbol' and 'type' columns, and other columns are aggregated accordingly. The 'time' column is converted to datetime format, and a new column 'Days Old' is calculated.

- Two Panel tables are created from the processed DataFrame: positions_summary and positions_all_grouped.

- A function update_table is defined to update the positions_all table with new data from the change stream.

- A new thread is started to listen to changes in the 'positions' collection in MongoDB and update the table accordingly.

- The script then creates a MetaApi instance, fetches the account and creates a streaming connection. It waits until synchronization is completed and fetches positions from the terminal state.

- The fetched positions are stored in MongoDB if they don't exist already.

- A FastGridTemplate is created with a dark theme, and the two Panel tables are added to the template's main area.

- Finally, the template is served in the browser using Panel's serve function. If the script is run as a standalone program, it will execute the main function asynchronously.

** What is missing is 'updates' to the positions data is NOT being handled.
- we need a plan for fetching updates on a regular interval that "updates" the mongodb and then updates the data in the tables
- we dont want to render new tables each time there is an update, we want to use the 'stream' and 'patch' features of tabulator to avoid total rebuilding of tables.


    
