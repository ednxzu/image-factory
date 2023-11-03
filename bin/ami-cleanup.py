import openstack
import sys
import openstack.exceptions as os_exceptions
import datetime
import re
import argparse
from tabulate import tabulate
from colorama import Fore, Style
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.validation import Validator, ValidationError
from tqdm import tqdm

# Custom validator for yes/no input
class YesNoValidator(Validator):
    def validate(self, document):
        text = document.text.lower()
        if text not in ('y', 'yes', 'n', 'no', ''):
            raise ValidationError(message="Please enter 'y', 'yes', 'n', or 'no'", cursor_position=len(document.text))

# Create a completer for "yes" and "no" responses
yes_no_completer = WordCompleter(["yes", "no"])

# Set mapping for the logos
logo_mapping = {
    "pass": f"{Fore.GREEN}✔{Style.RESET_ALL}",
    "outdated": f"{Fore.RED}✘{Style.RESET_ALL}",
    "warning": f"{Fore.YELLOW}⚠{Style.RESET_ALL}",
    "deleted": f"{Fore.RED}🗑️{Style.RESET_ALL}"
}

def create_parser():
    parser = argparse.ArgumentParser(
        description="Filter OpenStack images by name pattern using regex.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "--cloud", "-c",
        required=False,
        default="openstack",
        type=str,
        help="""
            The cloud config from the clouds.yaml file to use.
            The location can either be ~/.config/openstack/clouds.yaml or /etc/openstack/clouds.yaml.
        """
    )
    parser.add_argument(
        "--name", "-n",
        required=False,
        default=".*",
        type=str,
        help="""
            Regex pattern to match image names.
        """
    )
    parser.add_argument(
        "--remove-untagged", "-R",
        action="store_true",
        help="""
            In case you delete images, will also delete images that do not have the proper metadata.
        """
    )
    parser.add_argument(
        "--auto-approve", "-a",
        action="store_true",
        help="""
            Automatically approve image deletion
        """
    )
    return parser

def is_outdated(image):
    # Retrieve custom metadata tags added by Packer
    image_metadata = image.metadata

    # Check if both 'real_eol' and 'ednz_cloud_eol' tags are present in the custom metadata
    if 'official_eol' in image_metadata and 'ednz_cloud_eol' in image_metadata:
        official_eol_date = datetime.datetime.strptime(image_metadata['official_eol'], '%d/%m/%Y')
        ednz_cloud_eol_date = datetime.datetime.strptime(image_metadata['ednz_cloud_eol'], '%d/%m/%Y')

        # Check if either date has passed
        if official_eol_date < datetime.datetime.now() or ednz_cloud_eol_date < datetime.datetime.now():
            return "outdated"
        else:
            return "pass"

    # If either tag is missing, mark the image with a warning
    return "warning"

def delete_images(conn, image_ids):
    deleted_images = []
    for image_id in tqdm(image_ids, desc="Deleting images", unit=" image(s)"):
        try:
            conn.compute.delete_image(image_id)
            deleted_images.append(image_id)
        except os_exceptions.HttpException as e:
            print(f"HTTP Error while deleting image {image_id}: {e}")
        except os_exceptions.SDKException as e:
            print(f"SDK Error while deleting image {image_id}: {e}")
        except Exception as e:
            print(f"An unexpected error occurred while deleting image {image_id}: {e}")
        sys.stdout.flush()  # Update the console output
    return deleted_images

def print_deleted_image_table(delete_image_list, deleted_image_ids):
    deleted_table_headers = ["Deleted", "Image Name", "Image ID"]
    deleted_table_data = []
    for image in delete_image_list:
        if image.id in deleted_image_ids:
            deleted_table_data.append([logo_mapping.get("deleted"), image.name, image.id])
    print(tabulate(deleted_table_data, headers=deleted_table_headers, tablefmt="grid"))

def main(args):
    # Initialize and turn on debug logging
    openstack.enable_logging(debug=False)

    try:
        # Attempt to establish a connection to the OpenStack cloud
        conn = openstack.connect(cloud=args.cloud)
    except os_exceptions.HttpException as e:
        print(f"HTTP Error while connecting: {e}")
        # Handle the HTTP error (e.g., network issues)
    except os_exceptions.SDKException as e:
        print(f"SDK Error while connecting: {e}")
        # Handle the SDK-related error
    except os_exceptions.AuthorizationFailure as e:
        print(f"Authorization Failure while connecting: {e}")
        # Handle the authorization failure (e.g., incorrect credentials)
    except Exception as e:
        print(f"An unexpected error occurred while connecting: {e}")
        # Handle any other unexpected errors

    # Construct the regular expression pattern by appending -\d{8} to the argument value
    image_name_pattern = args.name

    # List images matching the regular expression pattern
    images = [image for image in conn.compute.images() if re.match(image_name_pattern, image.name)]

    # Prepare table headers and data
    table_headers = ["Pass", "Image Name", "Image ID", "Creation Date", "Status"]
    table_data = []

    # Prepare delete tables
    delete_image_list = []
    delete_image_list_full = []

    for image in images:
        created_at = datetime.datetime.strptime(image.created_at, '%Y-%m-%dT%H:%M:%SZ')
        status = is_outdated(image=image)
        image_pass = logo_mapping.get(status, None)
        # Add image to the table
        table_data.append([image_pass, image.name, image.id, created_at.strftime('%Y-%m-%d %H:%M:%S')])
        if (status == "outdated") or (status == "warning" and args.remove_untagged):
            delete_image_list.append(image.id)
            delete_image_list_full.append(image)

    # Print the table
    print(tabulate(table_data, headers=table_headers, tablefmt="grid"))

    # Prompt for deletion approval if not in auto-approve mode
    if delete_image_list:
        if not args.auto_approve:
            delete_approval = prompt("Do you want to delete the outdated images? (yes/no) [no]: ", completer=yes_no_completer)
            if delete_approval.lower() == 'yes':
                deleted_image_ids = delete_images(conn, delete_image_list)
                print_deleted_image_table(delete_image_list=delete_image_list_full, deleted_image_ids=deleted_image_ids)
            else:
                print("Images will not be deleted.")
        else:
            print("Auto-approve mode is enabled. Deleting images...")
            deleted_image_ids = delete_images(conn, delete_image_list)
            print_deleted_image_table(delete_image_list=delete_image_list_full, deleted_image_ids=deleted_image_ids)
    else:
        print("No outdated images to delete.")

if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()
    main(args)
