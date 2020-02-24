#block_storage_attached.py
#
# Checking for all block storage not attached not instances
#
#
#
# Parameter:
#                   profile_name
#           		(credentials are then picked up from the config file)
#
#
# Output:
#                    List of all Block volumes not attached to instances
#
#
#
# 30-jan-2030   Created     Mohamed Elkayal

import oci
import sys

# Get profile from command line
if len(sys.argv) == 2:
  profile = sys.argv[1]
else:
  profile='DEFAULT'

configfile = "Config Path"

config = oci.config.from_file(configfile, profile_name=profile)
identity = oci.identity.IdentityClient(config)
user = identity.get_user(config["user"]).data

print ("Logged in as: {} @ {}  (Profile={})".format(user.description, config["region"], profile))


regions = identity.list_region_subscriptions(config["tenancy"]).data
regions_list = []
attached_volumes = []
all_volumes = []
compartments = []

# Get regions aviliable
for region in regions:
    regions_list.append(region.region_name)

print("Enabled regions: {}".format(regions_list))

# Find all resources required
for region in regions_list:
    config['region'] = region
    compute_client = oci.core.ComputeClient(config)

    resource_search = oci.resource_search.ResourceSearchClient(config)
    query = '''query Instance, volume resources'''

    search_details = oci.resource_search.models.StructuredSearchDetails()
    search_details.query = query
    search_result = resource_search.search_resources(search_details=search_details, limit=1000).data

    for resource in search_result.items:
        compartment_id= resource.compartment_id
        instance_id=resource.identifier

        # Find all volumes available in this region
        if resource.resource_type == "Volume":
            all_volumes.append(resource)

        # Find all volumes attached to instances
        volume_attachments = oci.pagination.list_call_get_all_results(
            compute_client.list_volume_attachments,
            compartment_id=compartment_id,
            instance_id=instance_id
        ).data

        # Make sure there is volume aviliable before adding it to the list
        if len(volume_attachments)!= 0:
            for attached_volume in volume_attachments:
                attached_volumes.append(attached_volume.volume_id)

print("List of all Block volumes not attached to instances")
print("{:38} {:30} {}".format("Display name", "Compartment name", "Region"))

# Matchup the available volumes with the one attached
for volume in all_volumes:
    if volume.identifier not in attached_volumes and volume.lifecycle_state != "TERMINATED":
        compartment_name = identity.get_compartment(
            compartment_id=volume.compartment_id
        ).data
        print("{:38} {:30} {}".format(volume.display_name, compartment_name.name, volume.availability_domain))