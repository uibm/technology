#!/bin/bash

TAG_NAME=$(TZ=Asia/Kolkata date '+release-%Y%m%d-%H%M')
echo "tag_name=$TAG_NAME" >> $GITHUB_OUTPUT

echo "changelog<<EOF" >> $GITHUB_OUTPUT
echo "BBC Tech News Update ($(TZ=Asia/Kolkata date '+%Y-%m-%d %H:%M:%S IST'))" >> $GITHUB_OUTPUT
echo "" >> $GITHUB_OUTPUT
echo "✨ **What's New:**" >> $GITHUB_OUTPUT
if [ -f "_data/changelog.yml" ]; then
  echo "📰 New articles added in this update:" >> $GITHUB_OUTPUT
  grep "title:" _data/changelog.yml | head -n 5 | sed 's/title: /• /' >> $GITHUB_OUTPUT
  echo "" >> $GITHUB_OUTPUT
fi
echo "EOF" >> $GITHUB_OUTPUT
