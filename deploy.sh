#!/bin/bash
# Regenera el .ics y lo publica en GitHub Pages.
set -e
cd "$(dirname "$0")"
python3 make_ics.py

if [ ! -d .git ]; then
  git init -q -b main
  git remote add origin https://github.com/calmingsnakes/nat-bday.git
fi

git add -A
git commit -q -m "update: nat-bday calendar" || echo "(sin cambios que commitear)"
git push -q -u origin main
echo "push ok"
