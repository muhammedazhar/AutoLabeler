import json

def categorize_domains(domain_data):
    categories = {}
    
    # Add your domain-category mappings here
    category_mappings = {
        'Shopping': ['amazon.*', 'levi.*', 'zara.*'],
        'Banks': ['indusind.*', 'federalbank.*'],
        'University of Greenwich': ['gre.ac.uk', 'greenwich.ac.uk'],
        'Google': ['google.com'],
        'Project': ['github.com'],
        'Work': ['linkedin.com'],
        'Education': ['edu.com']
        # Add more categories and corresponding domains as needed
    }

    for category, domains in category_mappings.items():
        categories[category] = list(set(domains).intersection(domain_data))

    # Categorize remaining domains as 'Other'
    uncategorized_domains = set(domain_data) - set(domain for domains in categories.values() for domain in domains)
    categories['Other'] = list(uncategorized_domains)

    return categories

def update_categorised_json(categories, categorised_json_path):
    try:
        with open(categorised_json_path, 'r') as file:
            existing_categories = json.load(file)
    except FileNotFoundError:
        existing_categories = {}

    # Update existing categories with new data
    for category, domains in categories.items():
        existing_categories[category] = list(set(existing_categories.get(category, []) + domains))

    # Save the updated categories to 'categorised.json'
    with open(categorised_json_path, 'w') as file:
        json.dump(existing_categories, file, indent=2)

# Specify the path to your 'domains.json' file
domains_json_path = 'domains.json'

# Specify the path to save/update the 'categorised.json' file
categorised_json_path = 'categorised.json'

# Read domains from 'domains.json'
try:
    with open(domains_json_path, 'r') as file:
        domain_data = json.load(file)
except FileNotFoundError:
    print(f"Error: '{domains_json_path}' not found.")
    domain_data = []

# Categorize domains
categories = categorize_domains(domain_data)

# Update 'categorised.json' with the categorized domains
update_categorised_json(categories, categorised_json_path)

# Print the result
print("Categorization complete. Updated 'categorised.json'.")
