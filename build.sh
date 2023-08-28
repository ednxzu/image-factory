#! /bin/bash

##### functions #####
function get_packer_build_list {
  raw_list=($(tree "$(dirname $0)/ansible/inventory/production" -L 1 -J --noreport | jq -r .[].contents[].name))
  echo ${raw_list[@]%.*}
}

function main {
  shopt -s extglob
  build_list="@($(get_packer_build_list | sed -e 's/ /\|/g'))"

  case $BUILD_GROUP in
    $build_list)
      echo "#####  Building $BUILD_GROUP  #####"
      ansible-playbook -i ansible/inventory/production/$BUILD_GROUP.yml \
      ansible/01_generate_templates.yml \
      -e build_group=all
      ;;
    *)
      echo "No build_group specified or build_group does not exist. Aborting."
      ;;
  esac
}

##### execution #####
main "$@"