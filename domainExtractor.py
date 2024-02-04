import json
from pathlib import Path

def extract_domain(email):
    parts = email.split('@')
    return parts[1] if len(parts) == 2 else None

def extract_domains(emails):
    return {extract_domain(email) for email in emails if '@' in email}

def get_existing_domains():
    try:
        with open('domains.json', 'r') as file:
            return set(json.load(file))
    except FileNotFoundError:
        return set()

def save_domains(domains):
    existing_domains = get_existing_domains()

    # Add new domains to the set
    new_domains = domains - existing_domains
    existing_domains.update(domains)

    # Save the updated set back to 'domains.json'
    with open('domains.json', 'w') as file:
        json.dump(list(existing_domains), file, indent=2)

    return new_domains

# Check if 'domains.json' file exists
domains_file_path = 'domains.json'
domains_exist = Path(domains_file_path).is_file()

# Read emails from 'emails.json'
emails_file = Path('emails.json')
email_addresses = json.load(emails_file.open()) if emails_file.is_file() else []

# Extract domains
result = extract_domains(email_addresses)

# Save domains and get new domains
new_domains = save_domains(result)

# Print the result
if domains_exist:
    print(f"{len(new_domains)} new domains added to 'domains.json'.")
else:
    print(f"'domains.json' created with {len(result)} domains.")