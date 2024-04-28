import json
import os
import re

# Define common structure
common_structure = {
    "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
    "contentVersion": "1.0.0.0",
    "parameters": {"workspace": {"type": "String"}}
}

# Function to sanitize filenames
def sanitize_filename(name):
    # Remove invalid file characters
    return re.sub(r'[<>:"/\\|?*]', '', name)

# Load the large analytical rules JSON file
with open('analytical_rules.json', 'r') as file:
    data = json.load(file)

# Directory to save the single rule files
rules_dir = 'rules'
os.makedirs(rules_dir, exist_ok=True)

# Iterate through each rule in the 'resources' array
for rule in data["resources"]:
    display_name = rule["properties"]["displayName"]
    filename = f'{sanitize_filename(display_name)}.json'
    file_path = os.path.join(rules_dir, filename)
    
    # Merge common structure with rule details
    combined_rule_structure = common_structure.copy()
    combined_rule_structure["resources"] = [rule]
    
    # Write each rule as a separate JSON file
    with open(file_path, 'w', encoding='utf-8') as rule_file:
        json.dump(combined_rule_structure, rule_file, ensure_ascii=False, indent=4)

print(f"Exported {len(data['resources'])} rules to the '{rules_dir}' directory.")
