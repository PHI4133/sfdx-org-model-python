"""
  This script uses the SFDX git delta plugin to create the delta
  package. Then, it combines the delta XML file with the manual
  manifest XML file to create the final deployment package.
"""
import argparse
import logging
import subprocess
import sys

# import local scripts
import parse_package_file
import package_template

# Format logging message
logging.basicConfig(format='%(message)s', level=logging.DEBUG)


def parse_args():
    """
        Parse the required args
        from_ref - previous commit or baseline branch $CI_COMMIT_BEFORE_SHA
        to_ref - current commit or new branch $CI_COMMIT_SHA
        delta - delta file created by the SDFX Git Delta Plugin
            default file created by plugin is package/package.xml 
        manifest - manual manifest file in this repo
        combined - package.xml with delta and manifest updates combined
    """
    parser=argparse.ArgumentParser(description='A script to build the deploy package.')
    parser.add_argument('-f', '--from_ref')
    parser.add_argument('-t', '--to_ref')
    parser.add_argument('-d', '--delta', default='package/package.xml')
    parser.add_argument('-m', '--manifest', default='manifest/package.xml')
    parser.add_argument('-c', '--combined', default='deploy.xml')
    args=parser.parse_args()
    return args


def run_command(command):
    """
        Run the command using the system's command prompt (shell=True)
    """
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError:
        sys.exit(1)


def create_changes_dict(from_ref, to_ref, delta, manifest):
    """
        Run the plugin to create the delta file
        and add the changes from the delta file and manifest file
        to a dictionary.
    """
    run_command(f'sfdx sgd:source:delta --to "{to_ref}"'
                f' --from "{from_ref}" --output "."')
    # initialize changes dictionary
    changed = {}
    changed = parse_package_file.parse_package_xml(delta, changed)
    changed = parse_package_file.parse_package_xml(manifest, changed)
    return changed


def create_package_xml(items, output_file):
    """
        Create the final package.xml file
    """
    # Initialize the package contents with the header
    package_contents = package_template.PKG_HEADER

    # Append each item to the package
    for key in items:
        package_contents += "\t<types>\n"
        for member in items[key]:
            package_contents += "\t\t<members>" + member + "</members>\n"
        package_contents += "\t\t<name>" + key + "</name>\n"
        package_contents += "\t</types>\n"
    # Append the footer to the package
    package_contents += package_template.PKG_FOOTER
    logging.info('Deployment package contents:')
    logging.info(package_contents)
    with open(output_file, 'w', encoding='utf-8') as package_file:
        package_file.write(package_contents)


def main(from_ref, to_ref, delta, manifest, combined):
    """
        Main function to build the delta package
    """
    changes = create_changes_dict(from_ref, to_ref, delta, manifest)
    create_package_xml(changes, combined)


if __name__ == '__main__':
    inputs = parse_args()
    main(inputs.from_ref, inputs.to_ref,
         inputs.delta, inputs.manifest, inputs.combined)
