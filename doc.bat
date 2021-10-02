rmdir /s /q doc\build
mkdir doc\build\exec_directive
pipenv run sphinx-build -b html .\doc\source .\doc\build