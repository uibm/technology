#!/bin/bash

git config --local user.email "ujjwal.kumar1@ibm.com"
git config --local user.name "uibm"

echo "🕐 Commit time UTC: $(date -u)" >> commit_time.txt
echo "🇮🇳 Commit time IST: $(TZ=Asia/Kolkata date)" >> commit_time.txt
echo "✨ Enhanced with UI design" >> commit_time.txt

git add _data/changelog.yml index.html requirements.txt commit_time.txt

if ! git diff --quiet || ! git diff --staged --quiet; then
  git commit -m "🚀 Update changelog with UI [$(TZ=Asia/Kolkata date '+%Y-%m-%d %H:%M:%S IST')]\n\n✨ Features:\n- glassmorphism design\n- Dark theme with gradient backgrounds\n- Real-time search functionality\n- Category-based filtering\n- Smooth animations and transitions\n- Mobile-first responsive layout\n- Enhanced image handling\n- Performance optimizations\n\n📊 Stats: Updated with latest BBC Technology news"
  git push
fi
