This repository deals with two different file formats for Microsoft Sentinel Analytics Rules: YAML and ARM.

YAML format is used for distributing Analytics Rules among users, while ARM (JSON) format is required for deploying Analytics Rules in pipelines or importing them through the Microsoft Sentinel UI.

These formats have differences including resource type definition, property names, compare operators, and time formats. YAML focuses on being human-readable, so some deployment-related information like schema or APIVersion is omitted.

The image provided showcases a comparison of an Analytics Rule written in both YAML and as an ARM template, highlighting the differences between the two formats.


Introducing SentinelARConverter, a PowerShell module designed to ease the conversion between YAML and ARM formats for Microsoft Sentinel Analytics Rules.

The module consists of two functions:

Convert-SentinelARArmToYaml: Converts an ARM template into a valid YAML file.
Convert-SentinelARYamlToArm: Converts a YAML file into a valid ARM template.
Both functions work in the same manner. You can input a file and use the "UseOriginalFilename" switch, which converts the content and saves the resulting file with the same filename but with the opposite extension. This simplifies the process of converting Microsoft Sentinel Analytics Rules between the two formats.

Convert-SentinelARYamlToArm -Filename "C:\Users\User\Downloads\Azure_Sentinel_analytic_rule.yaml" -UseOriginalFilename


Get-Content "C:\Users\User\Downloads\Azure_Sentinel_analytic_rule.yaml" | Convert-SentinelARYamlToArm -OutFile "C:\Users\User\Downloads\Azure_Sentinel_analytic_rule.json" (You can also input the contents using the pipeline and define the exact output location using the OutFile parameter.)


Convert-SentinelARYamlToArm -Filename "C:\Users\User\Downloads\Azure_Sentinel_analytic_rule.yaml" (And if you don’t provide any output information it will return the converted file to the stdout.)



Convert-SentinelARYamlToArm -Filename "C:\Users\User\Downloads\Azure_Sentinel_analytic_rule.yaml" -UseOriginalFilename

Shoutout to Fabian who created the Powershell module https://cloudbrothers.info/en/convert-sentinel-analytics-rules/
