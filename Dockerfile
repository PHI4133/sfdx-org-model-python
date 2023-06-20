FROM ubuntu:latest

# Set Salesforce CLI Environment Variables - https://developer.salesforce.com/docs/atlas.en-us.sfdx_dev.meta/sfdx_dev/sfdx_dev_cli_env_variables.htm
ENV SFDX_AUTOUPDATE_DISABLE=true \
    # ^-- By default, the CLI periodically checks for and installs updates.
    #     Disable (false) this auto-update check to improve performance of CLI commands.
    SFDX_USE_GENERIC_UNIX_KEYCHAIN=true \
    # ^-- Set to true if you want to use the generic UNIX keychain instead of the Linux libsecret library or macOS keychain.
    #     Specify this variable when using the CLI with ssh or "headless" in a CI environment.
    SFDX_DOMAIN_RETRY=300 \
    # ^-- Specifies the time, in seconds, that the CLI waits for the Lightning Experience custom domain to resolve and become available in a newly-created scratch org.
    #     If you get errors about My Domain not configured when you try to use a newly-created scratch org, increase this wait time.
    SFDX_PROJECT_AUTOUPDATE_DISABLE_FOR_PACKAGE_CREATE=true \
    # ^-- For force:package:create, disables automatic updates to the sfdx-project.json file.
    SFDX_PROJECT_AUTOUPDATE_DISABLE_FOR_PACKAGE_VERSION_CREATE=true
    # ^-- For force:package:version:create, disables automatic updates to the sfdx-project.json file.

# Install nodejs, Salesforce CLI, git, sfdx-git-delta, and output information
RUN apt-get update && apt-get install -y curl git && \
    curl -fsSL https://deb.nodesource.com/setup_lts.x | bash - && \
    apt-get install -y nodejs && \
    npm install --global sfdx-cli@latest && \
    echo y | sfdx plugins:install sfdx-git-delta && \
    sfdx --version && \
    sfdx plugins --core && \
    uname -a && \
    node --version && \
    npm --version && \
    git --version
