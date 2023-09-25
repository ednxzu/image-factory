#! /bin/bash

##### variables #####
VAULT_ADDR=https://vault.ednz.fr
if [ "$TEST" != "true" ]; then
  unset VAULT_TOKEN
  if [ -z "$VAULT_ROLE_ID" ]; then
    echo "VAULT_ROLE_ID needs to be set in order to proceed"
    return 1
  fi

  if [ -z "$VAULT_SECRET_ID" ]; then
    echo "VAULT_SECRET_ID needs to be set in order to proceed"
    return 1
  fi
fi

##### functions #####
function get_packer_build_list {
  SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
  raw_list=($(tree "${SCRIPT_DIR}/ansible/inventory/production" -L 1 -J --noreport | jq -r .[].contents[].name))
  echo ${raw_list[@]%.*}
}

function vault_login_approle {
  curl --silent --request POST --data "{\"role_id\":\"${VAULT_ROLE_ID}\",\"secret_id\":\"${VAULT_SECRET_ID}\"}" $VAULT_ADDR/v1/auth/approle/login | jq -r .auth.client_token
}

function main {
  shopt -s extglob
  if [ "$TEST" != "true" ]; then
    export VAULT_ADDR=$VAULT_ADDR
    export VAULT_TOKEN=$(vault_login_approle)
  fi
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
      return 1
      ;;
  esac
}

##### execution #####
main "$@"