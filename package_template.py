"""
    Package.xml template
    Pull API version from api_version.py
"""
import os
from api_version import check_json_file

# get current API version used for the project
# only need the second return value
API_VERSION = check_json_file('./sfdx-project.json')[1]

# Set the project API version as an environment variable 
# to prevent the DNS lookup when the CLI tries to get the
# max API version from the org
os.environ["SFDX_API_VERSION"] = f'{API_VERSION}'

PKG_HEADER = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Package xmlns="http://soap.sforce.com/2006/04/metadata">
'''

PKG_FOOTER = f'''\t<version>{API_VERSION}</version>
</Package>
'''
