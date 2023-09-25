import openstack
import datetime
from tabulate import tabulate
from colorama import Fore, Style

# Initialize and turn on debug logging
openstack.enable_logging(debug=False)

# Initialize connection
conn = openstack.connect(cloud='ednz-lab')

# Define the image name pattern you want to search for
image_name_pattern = 'standard-ami-ubuntu-2204-24092023'

# Initialize the OpenStack connection
conn = openstack.connect(cloud='ednz-lab')

# Calculate the date 14 days ago
days_ago = datetime.datetime.now() - datetime.timedelta(days=14)

# List images matching the name pattern
images = conn.compute.images(name=image_name_pattern)

# Prepare table headers
table_headers = ["Pass", "Image Name", "Image ID", "Creation Date", "Status"]

# Prepare table data
table_data = []

# Check if the images are older than 14 days and format the table rows
for image in images:
    created_at = datetime.datetime.strptime(image.created_at, '%Y-%m-%dT%H:%M:%SZ')
    outdated = created_at < days_ago
    image_pass = f"{Fore.GREEN}✔{Style.RESET_ALL}" if not outdated else f"{Fore.RED}✘{Style.RESET_ALL}"
    status = f"UP TO DATE" if not outdated else f"OUTDATED"
    table_data.append([image_pass, image.name, image.id, created_at.strftime('%Y-%m-%d %H:%M:%S'), status])

# Print the table
print(tabulate(table_data, headers=table_headers, tablefmt="grid"))
