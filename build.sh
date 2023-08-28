#! /bin/bash

${BUILD_GROUP:?Please specify a build group}

ansible-playbook -i ansible/inventory/production/ansible-runners.yml \
  ansible/01_generate_templates.yml \
  -e build_group=ansible_docker_node
