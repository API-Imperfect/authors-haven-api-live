#!/usr/bin/env bash
 
set -o errexit
set -o pipefail
set -o nounset

working_dir="$(dirname ${0})"
source "${working_dir}/_sourced/constants.sh"
source "${working_dir}/_sourced/messages.sh"

message_welcome "These are the backups you have as at this point in time:"

ls -lht "${BACKUP_DIR_PATH}"