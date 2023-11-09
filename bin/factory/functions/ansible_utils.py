import os
import subprocess


def test_inventory(playbook_path, inventory_path):
    return


def generate_packer_files(playbook_path, inventory_path):
    return


def run_ansible_playbook(playbook_path, inventory_path):
    # Build the command to run the playbook
    command = [
        "ansible-playbook",
        playbook_path,
        "-i",
        inventory_path,
        "-e",
        "build_group=all",
    ]

    try:
        # Run the playbook using subprocess and capture the output
        result = subprocess.run(command)

        return result.stdout
    except subprocess.CalledProcessError as e:
        # Handle playbook execution failure
        return f"Playbook execution failed: {e.stderr}"
