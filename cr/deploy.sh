echo 'Running npm build'
npm run dev
echo 'Done...'

export PORT=8000
echo 'Server runnning on port ' $PORT
python3 ../manage.py runserver
