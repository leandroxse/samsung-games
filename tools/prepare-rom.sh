#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 2 ]]; then
  printf 'Uso: %s ROM_ORIGINAL.sfc PATCH.bps\n' "$0" >&2
  exit 2
fi

original=$1
patch=$2
root=$(cd -- "$(dirname -- "$0")/.." && pwd)
output="$root/roms/SMW-PTBR-2.0.sfc"

if ! command -v flips >/dev/null 2>&1; then
  printf 'Floating IPS (flips) não encontrado no PATH.\n' >&2
  exit 127
fi
if [[ ! -f "$original" || ! -f "$patch" ]]; then
  printf 'ROM original ou patch BPS não encontrado.\n' >&2
  exit 2
fi

mkdir -p "$root/roms"
flips --apply "$patch" "$original" "$output"
printf 'ROM preparada: %s\n' "$output"
