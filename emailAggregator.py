import re
import json
import os
import mailbox
import time

def extract_emails_and_content(mbox_file):
    emails = []
    email_content = {}

    mbox = mailbox.mbox(mbox_file)

    email_regex = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    pattern = re.compile(email_regex)

    start_time = time.time()  # Record start time

    for message in mbox:
        # Extract email address using regular expression
        sender_match = pattern.search(message['From'])
        if sender_match:
            sender = sender_match.group()
            emails.append(sender)

            # Extract email body content
            body = message.get_payload()
            email_content[sender] = body

    end_time = time.time()  # Record end time
    elapsed_time = end_time - start_time

    return emails, email_content, elapsed_time

def save_emails_to_json(emails, json_file):
    # Check if 'emails.json' file exists
    if os.path.isfile(json_file):
        # Read existing emails from 'emails.json' if the file exists
        with open(json_file, 'r') as file:
            existing_emails = json.load(file)
        # Append new emails to the list
        existing_emails.extend(emails)
        # Remove duplicates and maintain order
        unique_emails = list(dict.fromkeys(existing_emails))
    else:
        # If 'emails.json' doesn't exist, create a new file
        unique_emails = list(set(emails))

    with open(json_file, 'w') as file:
        json.dump(unique_emails, file, indent=2)

    return unique_emails

# Specify the path to your 'Inbox.mbox' file
mbox_file_path = 'Takeout/Mail/Inbox.mbox'

# Specify the path to save the 'emails.json' file
emails_json_file_path = 'emails.json'

# Check if 'Inbox.mbox' file exists
if not os.path.isfile(mbox_file_path):
    print(f"Error: '{mbox_file_path}' not found.")
else:
    # Extract email addresses and content
    extracted_emails, email_content, elapsed_time = extract_emails_and_content(mbox_file_path)

    # Save email addresses to 'emails.json' and get unique emails
    unique_emails = save_emails_to_json(extracted_emails, emails_json_file_path)

    # Print the result
    print(f"Total emails added to 'emails.json': {len(unique_emails)}")
    print(f"Time taken to read '{mbox_file_path}': {elapsed_time:.2f} seconds.")