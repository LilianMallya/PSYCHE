venv:
	python3.9 -m venv .venv39

install:
	. .venv39/bin/activate && pip install -r requirements.txt

test:
	. .venv39/bin/activate && pytest -q

run:
	. .venv39/bin/activate && streamlit run app.py
