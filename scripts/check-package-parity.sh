#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
package_root="$repo_root/dist/pkg/llm-prose-rules"
archive="$repo_root/dist/llm-prose-rules.zip"

if [[ ! -d "$package_root/styles" || ! -f "$archive" ]]; then
  echo "Missing packaged styles or release archive; run ./scripts/package-release.sh." >&2
  exit 1
fi

if ! diff -qr "$repo_root/styles" "$package_root/styles"; then
  echo "Packaged styles differ from source; run ./scripts/package-release.sh." >&2
  exit 1
fi

tmp_dir="$(mktemp -d)"
trap 'rm -rf "$tmp_dir"' EXIT
unzip -q "$archive" -d "$tmp_dir"

if ! diff -qr "$package_root" "$tmp_dir/llm-prose-rules"; then
  echo "Release archive differs from dist/pkg; run ./scripts/package-release.sh." >&2
  exit 1
fi
