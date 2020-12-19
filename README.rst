.. image:: https://readthedocs.org/projects/py-rsyslog-redis/badge/?version=latest
    :target: https://py-rsyslog-redis.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://app.codacy.com/project/badge/Grade/2622e60889dc4d649f3c35b06935549b
    :target: https://app.codacy.com/gh/augustoliks/py-rsyslog-redis

.. image:: https://codecov.io/gh/augustoliks/py-rsyslog-redis/branch/main/graph/badge.svg?token=EHJKGJKW3T
    :target: https://codecov.io/gh/augustoliks/py-rsyslog-redis

.. image:: https://travis-ci.com/augustoliks/py-rsyslog-redis.svg?branch=main
    :target: https://travis-ci.com/github/augustoliks/py-rsyslog-redis

py-rsyslog-redis
================

Rsyslog *omprog* plugin, propagate message logs for python instance. Rsylog (action) > Python (readlines) > Redis (pubsub channel)

Dependencies
------------

+--------------------+----------------------+
| Nome               | Versão               |
+====================+======================+
| redis              | 6.0                  |
+--------------------+----------------------+
| rsyslog            | 8.33.1               |
+--------------------+----------------------+
| python             | 3.7                  |
+--------------------+----------------------+
| python3-pip        | 19.1.1-8             |
+--------------------+----------------------+
| python3-virtualenv | 16.6.2-1             |
+--------------------+----------------------+

Setup
-----

.. code-block:: bash

    cd /opt/
    git clone https://github.com/augustoliks/py-rsyslog-redis/
    cd /opt/py-rsyslog-redis/
    virtualenv venv
    ./venv/bin/pip3 install redis
    cp rsyslog-config/30-pyrsyslogredis.conf /etc/rsyslog.d/
