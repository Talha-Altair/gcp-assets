from google.cloud import asset_v1
from dotenv import load_dotenv
import os
import json

load_dotenv(".env")

PROJECT_ID = os.getenv("PROJECT_ID")

project_resource = f"projects/{PROJECT_ID}"

supported_assets = {
    "compute.googleapis.com/Instance": "GCE VM",
    "sqladmin.googleapis.com/Instance": "CloudSQL Instance",
    "storage.googleapis.com/Bucket": "GCS Bucket",
    "secretmanager.googleapis.com/Secret": "Secret",
    "run.googleapis.com/Service": "Cloud Run Service",
    "pubsub.googleapis.com/Topic": "Pub-Sub Topic",
    "firestore.googleapis.com/Database": "Firestore Database",
    "bigquery.googleapis.com/Dataset": "BQ Dataset",
    "artifactregistry.googleapis.com/Repository": "AR Repo",
    "appengine.googleapis.com/Application": "AppEngine App",
}


def fetch_assets():

    client = asset_v1.AssetServiceClient()

    response = client.list_assets(request={"parent": project_resource})

    data = list(response)

    json_data = []

    for asset in data:

        if asset.asset_type not in supported_assets.keys():

            continue

        name = asset.name.split("/")[-1]

        desc = supported_assets[asset.asset_type]

        asset_data = {
            "URI": asset.name,
            "Type": asset.asset_type,
            "Name": name,
            "Description": desc,
        }

        json_data.append(asset_data)

    with open("data/data.json", "w") as f:

        json.dump(json_data, f)

    for data in json_data:

        print(f"{data['Description']}: {data['Name']} ")

if __name__ == "__main__":

    fetch_assets()
