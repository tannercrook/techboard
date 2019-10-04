#!/usr/bin/python
import sys
import logging
import os
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/techBoard/techBoard/")

from techBoard import app as application
application.secret_key = '\xfc\x123\xda\x06\xc8o\xf3\x95\x01\xafaU\\\xc1Z\xa4\xa9C\xddo\x020]'
