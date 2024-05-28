#!/usr/bin/env python3

import argparse
import os
import time
from pprint import pprint

import googleapiclient.discovery
import google.auth
from google.cloud import compute_v1

import re
import sys
from typing import Any
import warnings
from google.api_core.extended_operation import ExtendedOperation

credentials, project = google.auth.default()
service = googleapiclient.discovery.build('compute', 'v1', credentials=credentials)

#
# Stub code - just lists all instances
#
def list_instances(compute, project, zone):
    result = compute.instances().list(project=project, zone=zone).execute()
    return result['items'] if 'items' in result else None

# Referred https://github.com/GoogleCloudPlatform/python-docs-samples
def create_snapshot(
    project_id: str,
    disk_name: str,
    snapshot_name: str,
    zone: str = None,
    region: str = None,
    location: str = None,
    disk_project_id: str = None,
) -> compute_v1.Snapshot:
    
    if zone is None and region is None:
        raise RuntimeError(
            "You need to specify `zone` or `region` for this function to work."
        )
    if zone is not None and region is not None:
        raise RuntimeError("You can't set both `zone` and `region` parameters.")

    if disk_project_id is None:
        disk_project_id = project_id

    if zone is not None:
        disk_client = compute_v1.DisksClient()
        disk = disk_client.get(project=disk_project_id, zone=zone, disk=disk_name)
    else:
        regio_disk_client = compute_v1.RegionDisksClient()
        disk = regio_disk_client.get(
            project=disk_project_id, region=region, disk=disk_name
        )

    snapshot = compute_v1.Snapshot()
    snapshot.source_disk = disk.self_link
    snapshot.name = snapshot_name
    if location:
        snapshot.storage_locations = [location]

    snapshot_client = compute_v1.SnapshotsClient()
    snapshot_client.insert(project=project_id, snapshot_resource=snapshot)

    return snapshot_client.get(project=project_id, snapshot=snapshot_name)

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

project_id = "dsc-lab5-401501"
disk_name = "part1-vm1"
snapshot_name= "base-snapshot-part1-vm1"
zone = "us-west1-b"


# Referred https://github.com/GoogleCloudPlatform/python-docs-samples
def create_from_snapshot( project_id: str, zone: str, instance_name: str, snapshot_link: str ):
    disk_type = f"zones/{zone}/diskTypes/pd-standard"
    disks = [disk_from_snapshot(disk_type, 20, True, snapshot_link)]
    instance = create_instance(project_id, zone, instance_name, disks)
    return instance

# Referred https://github.com/GoogleCloudPlatform/python-docs-samples
def create_disk_from_snapshot(
    project_id: str,
    zone: str,
    disk_name: str,
    disk_type: str,
    disk_size_gb: int,
    snapshot_link: str,
) -> compute_v1.Disk:
    
    disk_client = compute_v1.DisksClient()
    disk = compute_v1.Disk()
    disk.zone = zone
    disk.size_gb = disk_size_gb
    disk.source_snapshot = snapshot_link
    disk.type_ = disk_type
    disk.name = disk_name
    disk_client.insert(project=project_id, zone=zone, disk_resource=disk)

    return disk_client.get(project=project_id, zone=zone, disk=disk_name)

# Referred https://github.com/GoogleCloudPlatform/python-docs-samples
def create_instance(
    project_id: str,
    zone: str,
    instance_name: str,
    disks: list[compute_v1.AttachedDisk],
    machine_type: str = "e2-medium",
    network_link: str = "global/networks/default",
    subnetwork_link: str = None,
    internal_ip: str = None,
    external_access: bool = True,
    external_ipv4: str = None,
    accelerators: list[compute_v1.AcceleratorConfig] = None,
    preemptible: bool = False,
    spot: bool = False,
    instance_termination_action: str = "STOP",
    custom_hostname: str = None,
    delete_protection: bool = False,
) -> compute_v1.Instance:
    
    instance_client = compute_v1.InstancesClient()

    startup_script = open(
        os.path.join(os.path.dirname(__file__), "../part1/startup-script.sh")
    ).read()

    # Use the network interface provided in the network_link argument.
    network_interface = compute_v1.NetworkInterface()
    network_interface.network = network_link
    if subnetwork_link:
        network_interface.subnetwork = subnetwork_link

    if internal_ip:
        network_interface.network_i_p = internal_ip

    if external_access:
        access = compute_v1.AccessConfig()
        access.type_ = compute_v1.AccessConfig.Type.ONE_TO_ONE_NAT.name
        access.name = "External NAT"
        access.network_tier = access.NetworkTier.PREMIUM.name
        if external_ipv4:
            access.nat_i_p = external_ipv4
        network_interface.access_configs = [access]

    # Collect information into the Instance object.
    instance = compute_v1.Instance()
    instance.metadata = {
            "items": [
                {
                    # Startup script is automatically executed by the
                    # instance upon startup.
                    "key": "startup-script",
                    "value": startup_script,
                }
            ]
        }
    instance.tags = {"items": ["allow-5000"]}
    instance.network_interfaces = [network_interface]
    instance.name = instance_name
    instance.disks = disks
    if re.match(r"^zones/[a-z\d\-]+/machineTypes/[a-z\d\-]+$", machine_type):
        instance.machine_type = machine_type
    else:
        instance.machine_type = f"zones/{zone}/machineTypes/{machine_type}"

    instance.scheduling = compute_v1.Scheduling()
    if accelerators:
        instance.guest_accelerators = accelerators
        instance.scheduling.on_host_maintenance = (
            compute_v1.Scheduling.OnHostMaintenance.TERMINATE.name
        )

    if preemptible:
        # Set the preemptible setting
        warnings.warn(
            "Preemptible VMs are being replaced by Spot VMs.", DeprecationWarning
        )
        instance.scheduling = compute_v1.Scheduling()
        instance.scheduling.preemptible = True

    if spot:
        # Set the Spot VM setting
        instance.scheduling.provisioning_model = (
            compute_v1.Scheduling.ProvisioningModel.SPOT.name
        )
        instance.scheduling.instance_termination_action = instance_termination_action

    if custom_hostname is not None:
        # Set the custom hostname for the instance
        instance.hostname = custom_hostname

    if delete_protection:
        # Set the delete protection bit
        instance.deletion_protection = True

    # Prepare the request to insert an instance.
    request = compute_v1.InsertInstanceRequest()
    request.zone = zone
    request.project = project_id
    request.instance_resource = instance

    # Wait for the create operation to complete.
    print(f"Creating the {instance_name} instance in {zone}...")

    operation = instance_client.insert(request=request)

    wait_for_extended_operation(operation, "instance creation")

    print(f"Instance {instance_name} created.")
    return instance_client.get(project=project_id, zone=zone, instance=instance_name)

# Referred https://github.com/GoogleCloudPlatform/python-docs-samples
def disk_from_snapshot(
    disk_type: str,
    disk_size_gb: int,
    boot: bool,
    source_snapshot: str,
    auto_delete: bool = True,
) -> compute_v1.AttachedDisk():

    disk = compute_v1.AttachedDisk()
    initialize_params = compute_v1.AttachedDiskInitializeParams()
    initialize_params.source_snapshot = source_snapshot
    initialize_params.disk_type = disk_type
    initialize_params.disk_size_gb = disk_size_gb
    disk.initialize_params = initialize_params
    # Remember to set auto_delete to True if you want the disk to be deleted when you delete
    # your VM instance.
    disk.auto_delete = auto_delete
    disk.boot = boot
    return disk

# Referred https://github.com/GoogleCloudPlatform/python-docs-samples
def wait_for_extended_operation(
    operation: ExtendedOperation, verbose_name: str = "operation", timeout: int = 300
) -> Any:
    result = operation.result(timeout=timeout)

    if operation.error_code:
        print(
            f"Error during {verbose_name}: [Code: {operation.error_code}]: {operation.error_message}",
            file=sys.stderr,
            flush=True,
        )
        print(f"Operation ID: {operation.name}", file=sys.stderr, flush=True)
        raise operation.exception() or RuntimeError(operation.error_message)

    if operation.warnings:
        print(f"Warnings during {verbose_name}:\n", file=sys.stderr, flush=True)
        for warning in operation.warnings:
            print(f" - {warning.code}: {warning.message}", file=sys.stderr, flush=True)

    return result

operation = create_snapshot(project_id, disk_name, snapshot_name, zone)

client = compute_v1.SnapshotsClient.from_service_account_json("/home/raan5764/lab-5-programmable-cloud-RAnandan10/part3/service-credentials.json")
snapshot = client.get(project=project_id, snapshot=snapshot_name)
status = snapshot.status

while status != 'READY':
    time.sleep(1)
    snapshot = client.get(project=project_id, snapshot=snapshot_name)
    status = snapshot.status

snapshot_link = f"projects/{project_id}/global/snapshots/{snapshot_name}"

for i in range(3):
    instance_name = f"part2-vm-from-snapshot-{i+1}"
    start_time = time.time()
    operation = create_from_snapshot(project_id,zone, instance_name, snapshot_link)
    print("Time taken to spin up instance", instance_name)
    print("--- %s seconds ---" % (time.time() - start_time))

print("Your running instances are:")
for instance in list_instances(service, project_id, 'us-west1-b'):
    print(instance['name'])