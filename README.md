# OCI_Block_Storage
This script is developed to get all volumes available in all regions, get all volumes attached to instances and then starts to matchup both together. 

The main purpose behind this script is to make sure that there are no unattached volumes, as in most cases when they are unattached they are not used so it is a good way to manage OCI.

This is just a reporting script that gives a list of all unattached volumes, the script doesn’t take any actions towards the volumes. 
