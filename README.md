Code examples from O'Reilly book - Lightweight Django, Using REST, WebSockets, and Backbone By Julia Elman, Mark Lavin

Requirements: Python3.4 then 
$ pip install -r requirements.txt
Note - one of these packages requires django-compress which should be automatically obtained using the pip command above. However if it fails, use the following commands:
$ pip install rcssmin --install-option="--without-c-extensions"
$ pip install rjsmin --install-option="--without-c-extensions"
$ pip install django-compressor --upgrade
