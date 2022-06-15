env PYTHON_CONFIGURE_OPTS="--enable-framework" pyenv install 3.9.2
pyenv local 3.9.2
pip install virtualenv poetry
virtualenv .venv
poetry install
python setup.py py2app
dist/main.app/Contents/MacOS/main