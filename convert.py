import re
import json
import chardet

def convert_arm_json_to_terraform(file_path):
    with open(file_path, 'rb') as file:
        raw_data = file.read()
        encoding = chardet.detect(raw_data)['encoding']
        arm_data = json.loads(raw_data.decode(encoding))

    resource = arm_data["resources"][0]
    properties = resource["properties"]

    query_text = properties['query'].strip()

    tactics = properties.get('tactics', [])
    tactics_tf = json.dumps(tactics) if tactics else "[]"

    techniques = properties.get('techniques', [])
    techniques_tf = json.dumps(techniques) if techniques else "[]"

    entity_mappings = properties.get('entityMappings', [])
    entity_mapping_blocks = []
    for mapping in entity_mappings:
        entity_type = mapping['entityType']
        field_mappings = mapping.get('fieldMappings', [])
        field_mapping_blocks = []
        for field_mapping in field_mappings:
            field_mapping_blocks.append(f'''
            field_mapping {{
              identifier = "{field_mapping['identifier']}"
              column_name = "{field_mapping['columnName']}"
            }}'''.strip())
        field_mappings_str = "\n".join(field_mapping_blocks)
        entity_mapping_blocks.append(f'''
        entity_mapping {{
          entity_type = "{entity_type}"
          {field_mappings_str}
        }}'''.strip())

    entity_mapping_tf = "\n".join(entity_mapping_blocks)

    terraform_code_template = '''resource "azurerm_sentinel_alert_rule_scheduled" "{resource_name}" {{
      name                       = "{name}"
      log_analytics_workspace_id = azurerm_log_analytics_workspace.TFWS.id
      display_name               = "{display_name}"
      severity                   = "{severity}"
      query                      = <<QUERY
{query}
      QUERY
      query_frequency            = "{query_frequency}"
      query_period               = "{query_period}"
      trigger_operator           = "{trigger_operator}"
      trigger_threshold          = {trigger_threshold}
      suppression_duration       = "{suppression_duration}"
      suppression_enabled        = {suppression_enabled}
      {tactics}
      {techniques}
      # Additional configuration here as needed
      {entity_mappings}
    }}
    '''

    terraform_code = terraform_code_template.format(
        resource_name=re.sub(r'\W', '_', properties['displayName']).lower(),
        name=properties['displayName'],
        display_name=properties['displayName'],
        severity=properties['severity'],
        query=query_text,
        query_frequency=properties['queryFrequency'],
        query_period=properties['queryPeriod'],
        trigger_operator=properties['triggerOperator'],
        trigger_threshold=properties['triggerThreshold'],
        suppression_duration=properties['suppressionDuration'],
        suppression_enabled=str(properties['suppressionEnabled']).lower(),
        tactics="tactics                    = " + tactics_tf,
        techniques="techniques                 = " + techniques_tf,
        entity_mappings=entity_mapping_tf
    )

    return terraform_code

# Replace 'your_arm_json_content_here' with the actual ARM JSON content
file_path = r'rules_json/CiscoASA-ThreatDetectionMessage.json'
terraform_code = convert_arm_json_to_terraform(file_path)
print("Terraform code generated:", terraform_code)  # Add a print statement to see the generated code

main_tf_file_path = 'main.tf'
with open(main_tf_file_path, 'a') as file:
    file.write(terraform_code + '\n')

print("Terraform code appended to", main_tf_file_path)  # Add a print statement to confirm the writing is successful