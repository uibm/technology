#!/bin/bash

TAG_NAME=$(TZ=Asia/Kolkata date '+release-%Y%m%d-%H%M')
echo "tag_name=$TAG_NAME" >> $GITHUB_OUTPUT

echo "changelog<<EOF" >> $GITHUB_OUTPUT
echo "🚀 BBC Tech News Update ($(TZ=Asia/Kolkata date '+%Y-%m-%d %H:%M:%S IST'))" >> $GITHUB_OUTPUT
echo "" >> $GITHUB_OUTPUT
echo "✨ **What's New:**" >> $GITHUB_OUTPUT
if [ -f "_data/changelog.yml" ]; then
  echo "📰 New articles added in this update:" >> $GITHUB_OUTPUT
  grep "title:" _data/changelog.yml | head -n 5 | sed 's/title: /• /' >> $GITHUB_OUTPUT
  echo "" >> $GITHUB_OUTPUT
  echo "🎨 **Premium UI Features:**" >> $GITHUB_OUTPUT
  echo "• Glassmorphism design with dark theme" >> $GITHUB_OUTPUT
  echo "• Real-time search and category filtering" >> $GITHUB_OUTPUT
  echo "• Smooth animations and micro-interactions" >> $GITHUB_OUTPUT
  echo "• Mobile-first responsive design" >> $GITHUB_OUTPUT
  echo "• Enhanced image loading and caching" >> $GITHUB_OUTPUT
fi
echo "EOF" >> $GITHUB_OUTPUT
