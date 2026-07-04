#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
dist_dir="$repo_root/dist"
package_root="$dist_dir/pkg/llm-prose-rules/styles"
package="$dist_dir/llm-prose-rules.zip"

rm -rf "$dist_dir"
mkdir -p "$package_root"

cp -R "$repo_root/styles/llm-prose-rules" "$package_root/"
cp -R "$repo_root/styles/llm-prose-rules-commits" "$package_root/"
cp -R "$repo_root/styles/llm-prose-rules-experimental" "$package_root/"
cp -R "$repo_root/styles/voice-dna" "$package_root/"
cp -R "$repo_root/styles/config" "$package_root/"

(
  cd "$dist_dir/pkg"
  zip -rq "$package" llm-prose-rules
)

echo "$package"
