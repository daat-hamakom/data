from os import environ

if 'PROD2' in environ:
	from .prod import *
else:
	from .local import *
