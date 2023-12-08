# positions table OLD PLAN

1. Data Fetching: We are using MetaApi's RPC for one-time requests to fetch initial data. For real-time updates, we are using MetaApi's Streaming API. This ensures that we always have the most up-to-date data.

2. Data Storage: We are storing the fetched data in MongoDB. This allows us to keep a historical record of the data, which is necessary for comparing metrics over time.

3. Data Usage: We are fetching the stored data from MongoDB as needed. This includes both the current data and historical data for comparison.

4. Real-Time Updates: We are using MongoDB's change streams feature to get real-time updates when the data changes. We are also using the stream method of the Panel Tabulator widget to update the front-end table in real-time.

5. Data Visualization: We are using Panel HoloViz for interactive data visualization. This allows us to present the data in a user-friendly way and update the visualizations in real-time.

6. Comparison Metrics: We are calculating certain metrics, such as the profit difference since yesterday or last week, based on the historical data stored in MongoDB. These metrics are updated each time new data is fetched.

This approach ensures that we always have the most up-to-date data, both for the current state and for historical comparisons. It also allows us to present the data in a user-friendly way and update the visualizations in real-time.