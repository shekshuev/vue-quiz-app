#!/bin/bash
unset VUE_APP_API_URL
unset FLASK_PORT
rm -rf ./dist
npm run build
cp ./static/questions.json ./dist/questions.json
pyinstaller --add-data "dist:static" server.py
rm ./server.spec
rm -rf ./build
mv ./dist/server ./build
rm -rf ./dist