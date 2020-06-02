# block_storage_attached.py
This script is developed to get all volumes available in all regions, get all volumes attached to instances and then starts to matchup both together. 

The main purpose behind this script is to make sure that there are no unattached volumes, as in most cases when they are unattached they are not used so it is a good way to manage OCI.

This is just a reporting script that gives a list of all unattached volumes, the script doesn’t take any actions towards these volumes. 

# psm&oci_resources.py
The script is designed to work with two CSVs files in which it will combine both of them into a new excel sheet. 

The script does few operations on the files sequentially as the following:
1.	Convert the two CSVs files into excel 
2.	Create new sheets on the original excel file 
3.	Copy the data from both files and add it to the original file
4.	Add AutoFilters to all columns 
5.	Add column AutoFit

This way a report will be automatically created and can be used directly without the need to do any manual changes. 

