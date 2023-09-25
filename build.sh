#! /bin/bash

##### variables #####
export VAULT_ADDR=https://vault.ednz.fr
if [[ $TEST -ne 'true' ]]; then
  unset VAULT_TOKEN
  ${VAULT_ROLE_ID:?VAULT_ROLE_ID needs to be set in order to proceed}
  ${VAULT_SECRET_ID:?VAULT_SECRET_ID needs to be set in order to proceed}
fi

##### functions #####
function get_packer_build_list {
  raw_list=($(tree "$(dirname $0)/ansible/inventory/production" -L 1 -J --noreport | jq -r .[].contents[].name))
  echo ${raw_list[@]%.*}
}

function vault_login_approle {
  export VAULT_TOKEN=$(curl --silent --request POST --data "{\"role_id\":\"${VAULT_ROLE_ID}\",\"secret_id\":\"${VAULT_SECRET_ID}\"}" \
  $VAULT_ADDR/v1/auth/approle/login | jq -r .auth.client_token)
}

#TODO
# curl --silent --request POST --data "{\"role_id\":\"${ROLE_ID}\",\"secret_id\":\"${SECRET_ID}\"}" https://vault.ednz.fr/v1/auth/approle/login | jq -r .auth.client_token

function main {
  shopt -s extglob
  if [[ $TEST -ne 'true' ]]; then
    vault_login_approle
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
      exit 1
      ;;
  esac
}

##### execution #####
main "$@"