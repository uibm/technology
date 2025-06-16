#!/bin/bash

git config --local user.email "ujjwal.kumar1@ibm.com"
git config --local user.name "uibm"

echo "🕐 Commit time UTC: $(date -u)" >> commit_time.txt
echo "🇮🇳 Commit time IST: $(TZ=Asia/Kolkata date)" >> commit_time.txt

git add _data/changelog.yml index.html requirements.txt commit_time.txt

if ! git diff --quiet || ! git diff --staged --quiet; then
  git commit -m "🚀 Update changelog with UI [$(TZ=Asia/Kolkata date '+%Y-%m-%d %H:%M:%S IST')] ✨ Features: 📊 Stats: Updated with latest BBC Technology news"
  git push
fi
