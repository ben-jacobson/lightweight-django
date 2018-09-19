import sys

from django.conf import settings

settings.configure(
    DEBUG=True,
    SECRET_KEY='d9rwza8$u_0+)3ob3ludg@^vua4+-hdjjj3^_jxz-z&0+t264+',
    ROOT_URLCONF='sitebuilder.urls',
    MIDDLEWARE_CLASSES=(),
    INSTALLED_APPS=(
        'django.contrib.staticfiles',
        'django.contrib.webdesign',
        'sitebuilder',
    ),
    STATIC_URL='/static/',
)

if __name__ == "__main__":
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)



# up to page 35