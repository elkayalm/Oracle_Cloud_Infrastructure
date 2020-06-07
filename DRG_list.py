# DRG_list.py
# List all DRGs created in an OCI tenancy
#
# 24-mar-2020	    Created         Mohamed Elkayal

import oci
import sys

# Get profile from command line
if len(sys.argv) == 2:
    profile = sys.argv[1]
else:
    profile = 'DEFAULT'

configfile = "~\\config"

config = oci.config.from_file(configfile, profile_name=profile)
identity = oci.identity.IdentityClient(config)
user = identity.get_user(config["user"]).data

print("Logged in as: {} @ {}  (Profile={})".format(user.description, config["region"], profile))

regions = identity.list_region_subscriptions(config["tenancy"]).data
regions_list = []

# Get regions available
for region in regions:
    regions_list.append(region.region_name)

print("Enabled regions: {}".format(regions_list))


# Traverse the returned object list to build the full compartment path
def traverse(compartments, parent_id, parent_path, compartment_list):
    next_level_compartments = [c for c in compartments if c.compartment_id == parent_id]
    for compartment in next_level_compartments:
        if compartment.name[0:17] != 'casb_compartment.' and compartment.lifecycle_state == 'ACTIVE':
            path = parent_path+'/'+compartment.name
            compartment_list.append(
                dict(id=compartment.id, name=compartment.name, path=path, state=compartment.lifecycle_state)
            )
            traverse(compartments, compartment.id, path, compartment_list)
    return compartment_list

def get_compartment_list(base_compartment_id):
    # Get list of all compartments below given base
    compartments = oci.pagination.list_call_get_all_results(
        identity.list_compartments, base_compartment_id,
        compartment_id_in_subtree=True).data

    # Got the flat list of compartments, now construct full path of each which makes it much easier to locate resources
    base_compartment_name = 'Root'
    base_path = '/root'

    compartment_list = [dict(id=base_compartment_id, name=base_compartment_name, path=base_path, state='Root')]
    compartment_list = traverse(compartments, base_compartment_id, base_path, compartment_list)
    compartment_list = sorted(compartment_list, key=lambda c: c['path'].lower())

    return compartment_list

# Find all resources required
for region in regions_list:
    config['region'] = region
    compartment_list = get_compartment_list(config['tenancy'])
    client = oci.core.VirtualNetworkClient(config)

    for compartment in compartment_list:
        drg = client.list_drgs(
            compartment_id=compartment['id'],
        ).data

        if len(drg) != 0:
            print(drg)
