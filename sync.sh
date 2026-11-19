#!/bin/bash
# Sync new files from Claude into this repo and push to GitHub.
# Usage: ./sync.sh "What changed"
# Picks up either ~/Downloads/Disruptor-update.zip (several files)
# or ~/Downloads/index.html (just the page).
set -e
cd "$(dirname "$0")"

ZIP="$HOME/Downloads/Disruptor-update.zip"
HTML="$HOME/Downloads/index.html"

if [ -f "$ZIP" ]; then
  rm -rf /tmp/disruptor-update
  unzip -q "$ZIP" -d /tmp/disruptor-update
  cp -R /tmp/disruptor-update/Disruptor-update/. .
  rm "$ZIP"
  echo "• Copied files from Disruptor-update.zip"
elif [ -f "$HTML" ]; then
  mv "$HTML" index.html
  echo "• Copied index.html"
else
  echo "✗ Nothing found in Downloads (Disruptor-update.zip or index.html)."
  exit 1
fi

chmod +x sync.sh
MSG="${1:-Update from Claude session}"
git add -A
if git diff --cached --quiet; then
  echo "✓ No changes. Already up to date."
  exit 0
fi
git commit -m "$MSG"
git push
echo "✓ Done: \"$MSG\" is now on your computer and on GitHub."
