echo 'Running npm build'
npm run build
echo 'Done...'

echo 'Deploying to Firebase'
firebase deploy
echo 'Done...'

open https://courseroad.co/
