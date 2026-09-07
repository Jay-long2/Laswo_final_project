#!/usr/bin/env bash
# Render build step. Exit immediately on any failure.
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

# First boot only: populate the portfolio and create the admin account.
# Both are no-ops once the site has content, so admin edits are never
# overwritten by a later deploy.
python manage.py seed_site --if-empty
python manage.py ensure_superuser
