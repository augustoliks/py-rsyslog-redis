test:
	poetry build
	poetry install
	export TEST_PY_RSYSLOG_REDIS=true; poetry run pytest --cov=pyrsyslogredis tests/

sphinx:
	cp README.rst docs/source/files/
	pip3 install -r docs/requirements.txt
	export TEST_PY_RSYSLOG_REDIS=true; sphinx-build -b html docs/source/ public/
	export TEST_PY_RSYSLOG_REDIS=true; sphinx-apidoc -o docs/source/modules/ pyrsyslogredis
