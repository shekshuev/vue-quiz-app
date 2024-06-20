@echo off

unset "VUE_APP_API_URL"
unset "FLASK_PORT"
DEL /S "%CD%\dist"
npm "run" "build"
COPY  "%CD%\static\questions.json" "%CD%\dist\questions.json"
pyinstaller "--add-data" "dist:static" "server.py"
DEL  "%CD%\server.spec"
DEL /S "%CD%\build"
mv "%CD%\dist\server" "%CD%\build"
DEL /S "%CD%\dist"