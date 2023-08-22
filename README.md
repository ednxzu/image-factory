# EDNZ Cloud ci-factory

This repository is my take at creating a fully automated container and images factory, using ansible and packer.
This is NOT ready for any kind of production use (yet), but it is the goal.

Example command to generate build files for all ansible_docker_node builds (node v16, v18, v20)
```bash
ansible-playbook -i ansible/inventory/production/ansible-runners.yml ansible/01_generate_templates.yml --extra-vars "build_group=ansible_docker_node"
```
