from os import environ

if 'PROD' in environ:
	from .prod import *
elif 'STAG' in environ:
	from .staging import *
else:
	from .local import *
