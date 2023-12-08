# Define the collections to fetch fields from
collections = ['positions', 'metrics', 'period_metrics', 'account_info']

# Open the output file
with open('records.txt', 'w') as f:
    # Fetch the first document from each collection and get all field names
    for collection in collections:
        doc = db[collection].find_one()
        fields = list(doc.keys())
        count = db[collection].count_documents({})

        # Write collection name, field names, and document count to the file
        f.write(f'Collection: {collection}\n')
        f.write(f'Fields: {", ".join(fields)}\n')
        f.write(f'Number of documents: {count}\n\n')

print("Fields and document counts have been written to 'records.txt'")