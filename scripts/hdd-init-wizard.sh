#!/usr/bin/env bash

# Human-facing decoration; keep protocol/data output unchanged.
cli_emoji() {
  [ "${CLI_PLAIN:-0}" = 1 ] || printf '%s ' "$1"
}
# Initialize a USB-attached SATA disk only after checking its identity and data.
set -Eeuo pipefail

dry_run=0
selected_disk=''
selected_majmin=''
selected_identity=''
system_known=0
declare -a system_disks=()

usage() {
  printf '%s' "$(cli_emoji '📖')"
  cat <<'EOF'
Usage: bash scripts/hdd-init-wizard.sh [--dry-run | --help]

Diagnose a USB SATA disk, then explicitly initialize it as GPT/ext4 and mount
it by UUID. Run as your normal login user; the wizard uses sudo only for
privileged operations. Initialization destroys the selected disk's partitions
and filesystem data. It is not a secure erase.

  --dry-run  Show diagnostics and planned operations without writing anything.
             In a terminal, you may select a disk for a detailed preview.
  --help     Show this help.
EOF
}

die() { printf '%sError: %s\n' "$(cli_emoji '❌')" "$*" >&2; exit 1; }
note() { printf '\n%s%s\n' "$(cli_emoji 'ℹ️')" "$*"; }

prompt() {
  local __name=$1 message=$2 input
  if ! IFS= read -r -p "$(cli_emoji '❓')$message" input; then
    die 'Input cancelled. No further changes made.'
  fi
  printf -v "$__name" '%s' "$input"
}

privileged() {
  if (( EUID == 0 )); then "$@"; else sudo "$@"; fi
}

show_privileged() {
  printf '  sudo'
  printf ' %q' "$@"
  printf '\n'
}

need() {
  local cmd
  for cmd in "$@"; do
    command -v "$cmd" >/dev/null 2>&1 || die "Required command missing: $cmd"
  done
}

is_system_disk() {
  local disk=$1 protected
  for protected in "${system_disks[@]}"; do
    [[ $protected == "$disk" ]] && return 0
  done
  return 1
}

discover_system_disks() {
  local mountpoint source majmin disk kind
  local -a ancestry=()
  for mountpoint in / /boot /boot/efi; do
    source=$(findmnt -nro SOURCE --mountpoint "$mountpoint" 2>/dev/null || true)
    [[ -n $source ]] || continue
    majmin=$(findmnt -nro MAJ:MIN --mountpoint "$mountpoint" 2>/dev/null || true)
    if [[ -n $majmin && -e /dev/block/$majmin ]]; then
      source="/dev/block/$majmin"
    fi
    mapfile -t ancestry < <(lsblk -s -nro PATH,TYPE "$source" 2>/dev/null || true)
    for line in "${ancestry[@]}"; do
      read -r disk kind <<< "$line"
      if [[ $kind == disk ]] && ! is_system_disk "$disk"; then
        system_disks+=("$disk")
      fi
    done
  done
  if ((${#system_disks[@]} > 0)); then system_known=1; fi
}

has_mounts() {
  local mounts
  mounts=$(lsblk -nr -o MOUNTPOINTS "$1" 2>/dev/null) || return 0
  [[ -n ${mounts//[[:space:]]/} ]]
}

disk_type_and_bus_ok() {
  [[ $(lsblk -dnro TYPE "$1" 2>/dev/null) == disk &&
     $(lsblk -dnro TRAN "$1" 2>/dev/null) == usb ]]
}

diagnostics() {
  local messages filtered
  note 'Detected block devices (diagnostics only):'
  lsblk -o NAME,PATH,SIZE,MODEL,SERIAL,TRAN,TYPE,FSTYPE,LABEL,MOUNTPOINTS

  note 'Recent USB/storage kernel messages:'
  messages=$(journalctl -k -n 160 --no-pager 2>/dev/null || true)
  [[ -n $messages ]] || messages=$(dmesg 2>/dev/null || true)
  filtered=$(printf '%s\n' "$messages" | grep -Ei 'usb|uas|scsi|sd[a-z]|ata|block|I/O error|reset' | tail -n 40 || true)
  if [[ -n $filtered ]]; then printf '%s\n' "$filtered"; else
    printf '%sNo readable recent USB/storage kernel messages.\n' "$(cli_emoji 'ℹ️')"
  fi

  note 'USB devices:'
  if command -v lsusb >/dev/null 2>&1; then
    lsusb || printf '%slsusb could not list devices.\n' "$(cli_emoji '❌')"
  else
    printf '%slsusb is unavailable (usbutils package); no package was installed.\n' "$(cli_emoji '❌')"
  fi

  if command -v smartctl >/dev/null 2>&1; then
    printf '\n%sSMART check available after disk selection (read-only).\n' "$(cli_emoji 'ℹ️')"
  else
    printf '\n%sSMART check unavailable. Install manually if wanted: sudo apt install smartmontools\n' "$(cli_emoji '❌')"
  fi
}

list_whole_disks() {
  local disk kind
  local -a rows=()
  note 'Whole disks (USB disks are the only selectable candidates):'
  mapfile -t rows < <(lsblk -dnro PATH,TYPE)
  for line in "${rows[@]}"; do
    read -r disk kind <<< "$line"
    [[ $kind == disk ]] || continue
    lsblk -dn -o PATH,SIZE,MODEL,SERIAL,TRAN,TYPE "$disk"
    if is_system_disk "$disk"; then
      printf '%s  BLOCKED: Ubuntu system/boot disk\n' "$(cli_emoji 'ℹ️')"
    elif has_mounts "$disk"; then
      printf '%s  BLOCKED: disk or child partition is mounted\n' "$(cli_emoji 'ℹ️')"
    elif ! disk_type_and_bus_ok "$disk"; then
      printf '%s  BLOCKED: not a USB-attached disk\n' "$(cli_emoji 'ℹ️')"
    else
      printf '%s  Candidate: confirm its exact full path to inspect it\n' "$(cli_emoji 'ℹ️')"
    fi
  done
}

inspect_selected() {
  local table signatures
  note "Selected disk: $selected_disk"
  lsblk -dn -o PATH,SIZE,MODEL,SERIAL,TRAN,TYPE,PTTYPE "$selected_disk"
  printf '%sPartition table: ' "$(cli_emoji 'ℹ️')"
  table=$(lsblk -dnro PTTYPE "$selected_disk")
  printf '%s\n' "${table:-none detected}"
  printf '%sDisk and child filesystems / mount state:\n' "$(cli_emoji 'ℹ️')"
  lsblk -o NAME,PATH,SIZE,TYPE,FSTYPE,LABEL,MOUNTPOINTS "$selected_disk"
  if (( dry_run )); then
    printf '%sSignatures: dry-run skips privileged signature inspection.\n' "$(cli_emoji 'ℹ️')"
    return
  fi
  signatures=$(privileged wipefs -n "$selected_disk") || die 'Cannot inspect disk signatures safely.'
  if [[ -n $signatures ]]; then printf '%sDisk signatures:\n%s\n' "$(cli_emoji 'ℹ️')" "$signatures"; fi
}

existing_data() {
  local table fstype child_types signatures
  table=$(lsblk -dnro PTTYPE "$selected_disk") || die 'Cannot read partition-table state.'
  fstype=$(lsblk -dnro FSTYPE "$selected_disk") || die 'Cannot read filesystem state.'
  child_types=$(lsblk -nro TYPE "$selected_disk") || die 'Cannot read partition state.'
  child_types=$(printf '%s\n' "$child_types" | grep -Ev '^disk$' || true)
  if [[ -n $table || -n $fstype || -n $child_types ]]; then return 0; fi
  if (( dry_run )); then return 1; fi
  signatures=$(privileged wipefs -n "$selected_disk") || die 'Cannot inspect disk signatures safely.'
  [[ -n $signatures ]]
}

check_mount_path() {
  local path=$1 contents
  [[ $path == /* && $path != / && $path =~ ^/[A-Za-z0-9._/-]+$ ]] ||
    die 'Mount path must be an absolute path without spaces or special characters.'
  [[ $path != *'//'* && $path != */../* && $path != */./* && $path != */.. && $path != */. ]] ||
    die 'Mount path must not contain repeated separators or dot components.'
  [[ ! -L $path ]] || die 'Mount path must not be a symlink.'
  [[ ! -e $path || -d $path ]] || die 'Mount path exists and is not a directory.'
  if [[ -d $path ]]; then
    contents=$(ls -A -- "$path") || die 'Cannot inspect mount path contents.'
    [[ -z $contents ]] || die 'Mount path is not empty.'
  fi
  if findmnt -n --mountpoint "$path" >/dev/null 2>&1; then
    die 'Mount path is already mounted.'
  fi
}

recheck_target() {
  [[ -b $selected_disk ]] || die 'Selected disk disappeared.'
  disk_type_and_bus_ok "$selected_disk" || die 'Selected disk is no longer a USB whole disk.'
  [[ $(lsblk -dnro MAJ:MIN "$selected_disk") == "$selected_majmin" ]] ||
    die 'Selected device identity changed; start again.'
  [[ $(lsblk -bdnro SIZE,MODEL,SERIAL "$selected_disk") == "$selected_identity" ]] ||
    die 'Selected disk size, model, or serial changed; start again.'
  discover_system_disks
  (( system_known )) || die 'Cannot identify the Ubuntu system disk; refusing to initialize any disk.'
  ! is_system_disk "$selected_disk" || die 'Selected disk is a system disk.'
  ! has_mounts "$selected_disk" || die 'Selected disk now has a mounted filesystem.'
}

partition_path() {
  local path kind
  local -a parts=() rows=()
  mapfile -t rows < <(lsblk -nrpo PATH,TYPE "$selected_disk")
  for line in "${rows[@]}"; do
    read -r path kind <<< "$line"
    [[ $kind == part ]] && parts+=("$path")
  done
  ((${#parts[@]} == 1)) || die "Expected one new partition; found ${#parts[@]}. Disk may be partially initialized."
  printf '%s' "${parts[0]}"
}

main() {
  local answer label mount_path owner uuid backup part expected_part existing=0 i
  case ${1:-} in
    --help|-h) usage; return 0 ;;
    --dry-run) dry_run=1 ;;
    '') ;;
    *) usage >&2; die 'Unknown option.' ;;
  esac
  (($# <= 1)) || die 'Use only one option.'
  need lsblk findmnt grep tail awk readlink
  if (( ! dry_run )); then
    [[ -t 0 ]] || die 'Interactive mode requires a terminal; use --dry-run for read-only diagnostics.'
    need sudo parted partprobe wipefs mkfs.ext4 blkid mount chown cp tee date df
  fi
  diagnostics
  discover_system_disks
  list_whole_disks
  if (( ! system_known )); then
    printf '\n%sUbuntu system disk could not be resolved. Initialization is disabled.\n' "$(cli_emoji '❌')"
  else
    printf '\n%sProtected system disk(s): %s\n' "$(cli_emoji 'ℹ️')" "${system_disks[*]}"
  fi
  local usb_count=0 disk kind
  while read -r disk kind; do
    if [[ $kind == disk ]] && disk_type_and_bus_ok "$disk"; then
      ((usb_count += 1))
    fi
  done < <(lsblk -dnro PATH,TYPE)
  if (( usb_count == 0 )); then
    printf '%sNo external SATA/USB disk detected. Check dock power, its power switch, USB cable, and try another USB port.\n' "$(cli_emoji 'ℹ️')"
    return 0
  fi
  if (( dry_run )) && [[ ! -t 0 ]]; then
    printf '\n%sDry run: no disk selected. Interactive preview would inspect a selected USB disk, then show:\n' "$(cli_emoji 'ℹ️')"
    printf '  sudo parted -s <disk> mklabel gpt\n  sudo parted -s -a optimal <disk> mkpart primary ext4 1MiB 100%%\n  sudo mkfs.ext4 -F -O 64bit -L Storage <new-partition>\n'
    printf '  sudo mkdir -p /mnt/storage; sudo mount <new-partition> /mnt/storage\n'
    printf '  sudo cp -p /etc/fstab <timestamped-backup>; append UUID entry; sudo mount -a\n'
    printf '%sNo writes were made.\n' "$(cli_emoji 'ℹ️')"
    return 0
  fi
  (( system_known )) || die 'Cannot safely distinguish the Ubuntu system disk.'

  prompt answer 'Type the exact full USB disk path to inspect (or press Enter to exit): '
  [[ -n $answer ]] || { printf '%sCancelled.\n' "$(cli_emoji 'ℹ️')"; return 0; }
  [[ $answer == /dev/* && -b $answer ]] || die 'That is not a full block-device path.'
  [[ $(readlink -f -- "$answer") == "$answer" ]] ||
    die 'Use the canonical full path shown in the whole-disk list.'
  [[ $(lsblk -dnro TYPE "$answer") == disk ]] || die 'Partitions cannot be selected.'
  selected_disk=$answer
  selected_majmin=$(lsblk -dnro MAJ:MIN "$selected_disk")
  selected_identity=$(lsblk -bdnro SIZE,MODEL,SERIAL "$selected_disk")
  [[ -n $selected_majmin && -n $selected_identity ]] || die 'Cannot establish the selected disk identity.'
  recheck_target
  inspect_selected
  prompt answer "Type $selected_disk exactly to confirm selection: "
  [[ $answer == "$selected_disk" ]] || die 'Selection confirmation did not match.'

  if command -v smartctl >/dev/null 2>&1; then
    prompt answer 'Run a non-destructive SMART check now? [y/N]: '
    if [[ $answer == y || $answer == Y ]]; then
      if (( dry_run )); then
        show_privileged smartctl -a -d sat "$selected_disk"
      else
        privileged smartctl -a -d sat "$selected_disk" ||
          printf '%sSMART check failed; this USB bridge may not pass SMART data.\n' "$(cli_emoji '❌')"
      fi
    fi
  fi

  if existing_data; then
    existing=1
    printf '\n%sExisting partitions or filesystem signatures may contain data.\n' "$(cli_emoji 'ℹ️')"
    printf '%s1) Exit\n2) Deliberately erase and reinitialize\n' "$(cli_emoji 'ℹ️')"
    prompt answer 'Choose 1 or 2: '
    [[ $answer == 2 ]] || { printf '%sExited without changes.\n' "$(cli_emoji 'ℹ️')"; return 0; }
    prompt answer "Type exactly 'ERASE $selected_disk': "
    [[ $answer == "ERASE $selected_disk" ]] || die 'Erase confirmation did not match.'
  fi

  prompt label 'Filesystem label [Storage]: '
  label=${label:-Storage}
  [[ $label =~ ^[A-Za-z0-9._-]{1,16}$ ]] || die 'Label must be 1–16 ASCII letters, digits, dots, underscores, or hyphens.'
  prompt mount_path 'Mount path [/mnt/storage]: '
  mount_path=${mount_path:-/mnt/storage}
  check_mount_path "$mount_path"
  if [[ $selected_disk == *[0-9] ]]; then
    expected_part="${selected_disk}p1"
  else
    expected_part="${selected_disk}1"
  fi
  owner=${SUDO_USER:-$(id -un)}
  [[ $owner != root ]] || die 'Run as a normal login user so mount ownership can be set safely.'

  note 'Planned privileged commands (partition path and UUID are determined after formatting):'
  if (( existing )); then show_privileged wipefs -a "$selected_disk"; fi
  show_privileged parted -s "$selected_disk" mklabel gpt
  show_privileged parted -s -a optimal "$selected_disk" mkpart primary ext4 1MiB 100%
  show_privileged partprobe "$selected_disk"
  show_privileged mkfs.ext4 -F -O 64bit -L "$label" "$expected_part"
  show_privileged mkdir -p "$mount_path"
  show_privileged mount "$expected_part" "$mount_path"
  show_privileged chown "$(id -u "$owner"):$(id -g "$owner")" "$mount_path"
  show_privileged cp -p /etc/fstab '/etc/fstab.backup-YYYYMMDD-HHMMSS'
  printf '  append: UUID=<new-uuid> %s ext4 defaults,nofail 0 2\n' "$mount_path"
  show_privileged mount -a
  if (( dry_run )); then printf '%sDry run complete. No writes were made.\n' "$(cli_emoji '✅')"; return 0; fi

  prompt answer "Final confirmation: type exactly 'INITIALIZE $selected_disk': "
  [[ $answer == "INITIALIZE $selected_disk" ]] || die 'Final confirmation did not match.'
  recheck_target
  if (( ! existing )) && existing_data; then
    die 'New disk signatures appeared; restart to inspect them.'
  fi
  # These operations replace the disk's partition table and filesystem.
  if (( existing )); then privileged wipefs -a "$selected_disk"; fi
  privileged parted -s "$selected_disk" mklabel gpt
  privileged parted -s -a optimal "$selected_disk" mkpart primary ext4 1MiB 100%
  privileged partprobe "$selected_disk"
  for i in {1..10}; do
    if [[ $(lsblk -nrpo PATH,TYPE "$selected_disk" | grep -c ' part$' || true) == 1 ]]; then break; fi
    sleep 1
  done
  part=$(partition_path)
  [[ $part == "$expected_part" ]] || die "Unexpected partition path $part; formatting stopped."
  privileged mkfs.ext4 -F -O 64bit -L "$label" "$part"
  uuid=$(privileged blkid -s UUID -o value "$part")
  [[ -n $uuid ]] || die 'Formatted partition has no readable UUID; fstab was not changed.'
  check_mount_path "$mount_path"
  [[ -r /etc/fstab ]] || die 'Cannot inspect /etc/fstab before editing it.'
  if awk -v p="$mount_path" -v u="UUID=$uuid" '$1 !~ /^#/ && ($1 == u || $2 == p) { found=1 } END { exit !found }' /etc/fstab; then
    die 'fstab already contains this UUID or mount path.'
  fi

  privileged mkdir -p -- "$mount_path"
  privileged mount "$part" "$mount_path"
  privileged chown "$(id -u "$owner"):$(id -g "$owner")" "$mount_path"
  backup="/etc/fstab.backup-$(date +%Y%m%d-%H%M%S)"
  [[ ! -e $backup ]] || die "Backup already exists: $backup"
  privileged cp -p /etc/fstab "$backup"
  if ! printf 'UUID=%s %s ext4 defaults,nofail 0 2\n' "$uuid" "$mount_path" |
      privileged tee -a /etc/fstab >/dev/null; then
    privileged cp -p "$backup" /etc/fstab || die "fstab append failed and restore failed; restore manually from $backup"
    die "fstab append failed. Restored /etc/fstab from $backup; disk remains formatted and mounted."
  fi
  if ! privileged mount -a; then
    privileged cp -p "$backup" /etc/fstab || die "mount -a failed and fstab restore failed; restore manually from $backup"
    die "mount -a failed. Restored /etc/fstab from $backup; disk remains formatted and mounted."
  fi

  note 'Initialization complete:'
  lsblk -o NAME,PATH,SIZE,MODEL,SERIAL,TRAN,TYPE,FSTYPE,LABEL,MOUNTPOINTS "$selected_disk"
  df -h "$mount_path"
  printf '%sUUID: %s\nLabel: %s\nMount point: %s\nfstab backup: %s\n' "$(cli_emoji 'ℹ️')" "$uuid" "$label" "$mount_path" "$backup"
}

main "$@"
