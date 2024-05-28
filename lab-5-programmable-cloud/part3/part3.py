#!/usr/bin/env python3

import argparse
import os
import time
from pprint import pprint

import googleapiclient.discovery
import google.auth
import google.oauth2.service_account as service_account

#
# Use Google Service Account - See https://google-auth.readthedocs.io/en/latest/reference/google.oauth2.service_account.html#module-google.oauth2.service_account
#
credentials = service_account.Credentials.from_service_account_file(filename="/home/raan5764/lab-5-programmable-cloud-RAnandan10/part3/service-credentials.json")
project = os.getenv('GOOGLE_CLOUD_PROJECT') or 'dsc-lab5-401501'
service = googleapiclient.discovery.build('compute', 'v1', credentials=credentials)
project_id = "dsc-lab5-401501"
#
# Stub code - just lists all instances
#
def list_instances(compute, project, zone):
    result = compute.instances().list(project=project, zone=zone).execute()
    return result['items'] if 'items' in result else None

# Referred https://github.com/GoogleCloudPlatform/python-docs-samples
def create_instance( compute: object, project: str, zone: str, name: str, bucket: str ) -> str:
    # Get the latest Ubuntu image.
    image_response = (
        compute.images()
        .getFromFamily(project="ubuntu-os-cloud", family="ubuntu-2204-lts")
        .execute()
    )
    source_disk_image = image_response["selfLink"]

    # Configure the machine
    machine_type = "zones/%s/machineTypes/e2-medium" % zone
    vm2_startup_script = open(
        os.path.join(os.path.dirname(__file__), "../part1/startup-script.sh")
    ).read()

    service_credentials = open(
        os.path.join(os.path.dirname(__file__), "service-credentials.json")
    ).read()

    vm1_startup_script = open(
        os.path.join(os.path.dirname(__file__), "startup-script-vm1.sh")
    ).read()

    vm2_launch_code = open(
        os.path.join(os.path.dirname(__file__), "vm2_launch_code.py")
    ).read()

    config = {
        "name": name,
        #"tags" : {"items": ["allow-5000"]},
        "machineType": machine_type,
        # Specify the boot disk and the image to use as a source.
        "disks": [
            {
                "boot": True,
                "autoDelete": True,
                "initializeParams": {
                    "sourceImage": source_disk_image,
                },
            }
        ],
        # Specify a network interface with NAT to access the public
        # internet.
        "networkInterfaces": [
            {
                "network": "global/networks/default",
                "accessConfigs": [{"type": "ONE_TO_ONE_NAT", "name": "External NAT"}],
            }
        ],
        # Allow the instance to access cloud storage and logging.
        "serviceAccounts": [
            {
                "email": "default",
                "scopes": [
                    "https://www.googleapis.com/auth/devstorage.read_write",
                    "https://www.googleapis.com/auth/logging.write",
                ],
            }
        ],
        # Metadata is readable from the instance and allows you to
        # pass configuration from deployment scripts to instances.
        "metadata": {
            "items": [
                {
                    # Startup script is automatically executed by the
                    # instance upon startup.
                    "key": "startup-script",
                    "value": vm1_startup_script,
                },
                {   "key": "bucket", 
                    "value": bucket
                },
                {   "key": "service-credentials", 
                    "value": service_credentials
                },
                {   "key": "vm2-startup-script", 
                    "value": vm2_startup_script
                },
                {   "key": "vm1-launch-vm2-code", 
                    "value": vm2_launch_code
                }
            ]
        },
    }
    print("Creating instance", name)
    return compute.instances().insert(project=project, zone=zone, body=config).execute()

# Referred https://github.com/GoogleCloudPlatform/python-docs-samples
def wait_for_operation( compute: object, project: str, zone: str, operation: str) -> dict:
    
    print("Waiting for operation to finish...")
    while True:
        result = (
            compute.zoneOperations()
            .get(project=project, zone=zone, operation=operation)
            .execute()
        )

        if result["status"] == "DONE":
            print("done.")
            if "error" in result:
                raise Exception(result["error"])
            return result

        time.sleep(1)
    print("Operation finished...")

zone = "us-west1-b"
instance_name = "part3-vm1-test"
bucket = "test-bucket"

operation = create_instance(service, project, zone, instance_name, bucket)
wait_for_operation(service, project, zone, operation["name"])

print("Your running instances are:")
for instance in list_instances(service, project, 'us-west1-b'):
    print(instance['name'])