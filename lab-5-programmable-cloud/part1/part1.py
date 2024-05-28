#!/usr/bin/env python3

import argparse
import os
import time
from pprint import pprint

import googleapiclient.discovery
import google.auth

from google.cloud import compute_v1

credentials, project = google.auth.default()
service = googleapiclient.discovery.build('compute', 'v1', credentials=credentials)

#
# Stub code - just lists all instances
#
def list_instances(compute, project, zone):
    result = compute.instances().list(project=project, zone=zone).execute()
    return result['items'] if 'items' in result else None

#Referred https://github.com/GoogleCloudPlatform/python-docs-samples
def create_instance(
    compute: object,
    project: str,
    zone: str,
    name: str,
    bucket: str,
) -> str:
    # Get the latest Ubuntu image.
    image_response = (
        compute.images()
        .getFromFamily(project="ubuntu-os-cloud", family="ubuntu-2204-lts")
        .execute()
    )
    source_disk_image = image_response["selfLink"]

    # Configure the machine
    machine_type = "zones/%s/machineTypes/e2-medium" % zone
    startup_script = open(
        os.path.join(os.path.dirname(__file__), "startup-script.sh")
    ).read()

    config = {
        "name": name,
        "tags" : {"items": ["allow-5000"]},
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
                    "value": startup_script,
                },
                {"key": "bucket", "value": bucket},
            ]
        },
    }

    return compute.instances().insert(project=project, zone=zone, body=config).execute()

#Referred https://github.com/GoogleCloudPlatform/python-docs-samples
def wait_for_operation(
    compute: object,
    project: str,
    zone: str,
    operation: str,
) -> dict:
    """Waits for the given operation to complete.

    Args:
      compute: an initialized compute service object.
      project: the Google Cloud project ID.
      zone: the name of the zone in which the operation should be executed.
      operation: the operation ID.

    Returns:
      The result of the operation.
    """
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

#Referred https://github.com/GoogleCloudPlatform/python-docs-samples
def create_firewall_rule(
    project_id: str, firewall_rule_name: str, network: str = "global/networks/default"
) -> compute_v1.Firewall:

    firewall_rule = compute_v1.Firewall()
    firewall_rule.name = firewall_rule_name
    firewall_rule.direction = "INGRESS"

    allowed_ports = compute_v1.Allowed()
    allowed_ports.I_p_protocol = "tcp"
    allowed_ports.ports = ["5000"]

    firewall_rule.allowed = [allowed_ports]
    firewall_rule.source_ranges = ["0.0.0.0/0"]
    firewall_rule.network = network
    firewall_rule.description = "Allowing TCP traffic on port 5000 from Internet."

    firewall_rule.target_tags = ["allow-5000"]
    
    firewall_client = compute_v1.FirewallsClient()
    firewall_client.insert(
        project=project_id, firewall_resource=firewall_rule
    )

    return firewall_client.get(project=project_id, firewall=firewall_rule_name)

zone = "us-west1-b"
instance_name = "part1-vm1"
bucket = "test-bucket"
project = "dsc-lab5-401501"

operation = create_instance(service, project, zone, instance_name, bucket)
wait_for_operation(service, project, zone, operation["name"])
create_firewall_rule(project, "allow-5000")

print("Your running instances are:")
for instance in list_instances(service, project, 'us-west1-b'):
    print(instance['name'])
