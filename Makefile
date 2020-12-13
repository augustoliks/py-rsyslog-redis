test:
	poetry build
	poetry install
	export TEST_PY_RSYSLOG_REDIS=true; poetry run pytest --cov=pyrsyslogredis tests/

sphinx:
	mkdir -p docs/source/files
	mkdir -p docs/source/modules
	cp README.rst docs/source/files/
	cp RELEASE-NOTES.rst docs/source/files/
# 	pip3 install -r docs/requirements.txt
	sphinx-build -b html docs/source/ public/
	sphinx-apidoc -o docs/source/modules/ pyrsyslogredis
