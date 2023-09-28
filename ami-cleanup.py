import openstack
import datetime
import re
import argparse
from tabulate import tabulate
from colorama import Fore, Style

# Initialize and turn on debug logging
openstack.enable_logging(debug=False)

# Initialize connection
conn = openstack.connect(cloud='openstack')

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Filter OpenStack images by name pattern using regex.")
parser.add_argument("image_name_pattern", help="Regex pattern to match image names")
args = parser.parse_args()

# Construct the regular expression pattern by appending -\d{8} to the argument value
image_name_pattern = args.image_name_pattern + r'-\d{8}'

# Calculate the date 14 days ago
days_ago = datetime.datetime.now() - datetime.timedelta(days=14)

# List images matching the regular expression pattern
images = [image for image in conn.compute.images() if re.match(image_name_pattern, image.name)]

# Prepare table headers
table_headers = ["Pass", "Image Name", "Image ID", "Creation Date", "Status"]

# Prepare table data
table_data = []

# Check if the images are older than 14 days
for image in images:
    created_at = datetime.datetime.strptime(image.created_at, '%Y-%m-%dT%H:%M:%SZ')
    outdated = created_at < days_ago
    image_pass = f"{Fore.GREEN}✔{Style.RESET_ALL}" if not outdated else f"{Fore.RED}✘{Style.RESET_ALL}"
    # status = f"UP TO DATE" if not outdated else f"OUTDATED"
    table_data.append([image_pass, image.name, image.id, created_at.strftime('%Y-%m-%d %H:%M:%S')])

# Print the table
print(tabulate(table_data, headers=table_headers, tablefmt="grid"))
