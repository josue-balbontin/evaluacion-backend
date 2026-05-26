
set -e

echo "Waiting for Postgres..."
while ! python -c "
import psycopg2, os
psycopg2.connect(
    dbname=os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    host=os.getenv('DB_HOST', 'postgres'),
    port=os.getenv('DB_PORT', '5432')
)
" 2>/dev/null; do
    sleep 1
done
echo "Postgres is ready."


python -c "
import psycopg2, os
conn = psycopg2.connect(
    dbname=os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    host=os.getenv('DB_HOST', 'postgres'),
    port=os.getenv('DB_PORT', '5432')
)
conn.autocommit = True
cur = conn.cursor()
cur.execute('CREATE SCHEMA IF NOT EXISTS content')
cur.close()
conn.close()
"
echo "Schema 'content' ensured."


echo "Running migrations..."
python manage.py migrate --noinput


echo "Collecting static files..."
python manage.py collectstatic --noinput


echo "Creating superuser..."
python manage.py createsuperuser --noinput 2>/dev/null || echo "Superuser already exists."


echo "Seeding data..."
python manage.py seed_data 2>/dev/null || echo "Data already seeded or seed command not found."


echo "Starting Gunicorn..."
exec gunicorn core.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --timeout 30 \
    --access-logfile - \
    --error-logfile -
