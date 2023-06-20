#!/bin/bash
# $DEPLOY_LOG passed in from YAML
# Check if validation log exists
if [ ! -f $DEPLOY_LOG ]; then
  echo "Error: Validation log not found."
  exit 1
fi

# Pull deployment ID from the validation log
deploy_id=$(grep -rnw $DEPLOY_LOG -e 'Deploy ID:' | sed 's/..*Deploy ID: //g')

# Check if deploy ID is empty
if [ -z "$deploy_id" ]; then
  echo "Error: Unable to find Deploy ID in the validation log."
  exit 1
fi

echo "Running quick deploy for $deploy_id"
sfdx force:source:deploy -q $deploy_id -w $DEPLOY_TIMEOUT
