SHELL := /bin/bash

init-unix:
    python3 -m venv venv
    source venv/bin/activate; \
    pip install -r requirements.txt

init-windows:
    py -m venv venv
    .\venv\Scripts\activate; \
    pip install -r requirements.txt