import json
import requests
import hashlib
import psycopg2
from bs4 import BeautifulSoup
from datetime import date 

# Function to mask PII
def mask_pii(value):
    """
    Masks personally identifiable information (PII) using SHA-256 hash.

    Parameters:
    value (str): The string value to be masked.

    Returns:
    str: The hashed value.
    """
    return hashlib.sha256(value.encode()).hexdigest()

# Connect to Postgres
try:
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()
    print("Connected to Postgres")
except Exception as e:
    print(f"Failed to connect to Postgres: {e}")
    exit()

def insert_record(record):
    try:
        query = """
        INSERT INTO user_logins (user_id, device_type, masked_ip, masked_device_id, locale, app_version, create_date)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cur.execute(query, record)
        conn.commit()
        print(f"Inserted record: {record}")
    except Exception as e:
        print(f"Failed to insert record: {e}")

# Fetch message from SQS
try:
    response = requests.post("http://localhost:4566/000000000000/login-queue", data={'Action': 'ReceiveMessage'})
    print(f"Fetched messages, status code: {response.status_code}")
except requests.exceptions.RequestException as e:
    print(f"Error: {e}")
    exit()

# Check if the response is successful
if response and response.status_code == 200:
    try:
        # Parse XML response using BeautifulSoup
        soup = BeautifulSoup(response.content, 'xml')
        messages = soup.find_all("Message")
        print(f"Number of messages received: {len(messages)}")

        # Process each message
        for message in messages:
            # Extract message body using BeautifulSoup
            body_element = message.find("Body")
            if body_element:
                body = body_element.text
                print("Extracted message body:", body)
                data = json.loads(body)

                app_version_numeric = ''.join(filter(str.isdigit, data['app_version']))

                # transformed data
                record = (
                    data['user_id'],
                    data['device_type'],
                    mask_pii(data['ip']),
                    mask_pii(data['device_id']),
                    data['locale'],
                    int(app_version_numeric), 
                    date.today()
                )

                insert_record(record)
            else:
                print("Error: Message body not found")

    except (json.JSONDecodeError, Exception) as e:
        print(f"Error: {e}")

else:
    if response:
        print(f"Error: Failed to fetch messages, status code {response.status_code}")

# Close the cursor and connection
cur.close()
conn.close()
print("Closed connection to Postgres")
