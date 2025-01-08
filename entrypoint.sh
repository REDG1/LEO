#!/bin/bash
# The --login ensures the bash configuration is loaded,
# enabling Conda.

# Enable strict mode.
set -euo pipefail
# ... Run whatever commands ...

# Temporarily disable strict mode and activate conda:
set +euo pipefail

# Activate the Conda environment
echo "Activating Conda environment..."
source /opt/conda/etc/profile.d/conda.sh
source activate omeroScripts

# Re-enable strict mode:
set -euo pipefail

echo "Checking MySQL..."
python sql_check.py || exit 1
echo "Apply migrations..."
nginx && python manage.py makemigrations --noinput && python manage.py migrate --noinput && python manage.py collectstatic --noinput --clear
echo "Loading initial data providers..."
python manage.py loaddata initialData.json
echo "running server..."
gunicorn LEO.wsgi:application --bind 0.0.0.0:5001 --timeout 800