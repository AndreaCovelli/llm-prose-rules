#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
dist_dir="$repo_root/dist"
package="$dist_dir/llm-prose-rules.zip"

rm -rf "$dist_dir"
mkdir -p "$dist_dir"

(
  cd "$repo_root/styles"
  zip -rq "$package" \
    llm-prose-rules \
    llm-prose-rules-commits \
    llm-prose-rules-experimental \
    voice-dna \
    config
)

echo "$package"
