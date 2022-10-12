import csv
import json

filename = "liveoak-tech"
with open(f'{filename}.json', 'r') as jsonfile:
    data = json.load(jsonfile)

csv_dict = {}

with open(f'{filename}.csv', 'w') as f:
    wr = csv.writer(f, delimiter=",")
    writer = csv.DictWriter(f, fieldnames=['AWS Region', 'Repository Name', 'Description', 'ECR Policy'])
    writer.writeheader()
    regions = ["us-west-2", "us-east-1", "us-east-2", "eu-west-1"]

    for region in regions:
        for key,value in data.items():
            if region in key:
                repos = value
                for repo in repos:
                    writer.writerow({'AWS Region': region, 'Repository Name': repo['repositoryName'], 'Description': repo['description'], 'ECR Policy': ""})