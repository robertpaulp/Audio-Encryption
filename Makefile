PYTHON = python3
PIP = pip3
PROJECT_NAME = main.py

install:
	$(PIP) install -r requirements.txt

clean:
	rm -rf __pycache__