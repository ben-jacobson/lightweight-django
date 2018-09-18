import os
import sys
from django.conf import settings

DEBUG = os.environ.get('DEBUG', 'on') == 'on'
SECRET_KEY = os.environ.get('SECRET_KEY', 'q$%a_tg%ty(5feo+sy9v$36+ncrupv8tt-9&=a1^l__3&xak@w')
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost').split(',')

settings.configure(
    DEBUG=DEBUG,
    SECRET_KEY=SECRET_KEY,
    ALLOWED_HOSTS=ALLOWED_HOSTS,
    ROOT_URLCONF=__name__,
    MIDDLEWARE_CLASSES=(
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',                           
    ),
)

from django import forms
from django.conf.urls import url
from django.core.cache import cache             # django has a great caching framework built in, very simple to use. To cache something is to save the result of an expensive calculation so that you don’t have to perform the calculation next time. You can cache the output of specific views, you can cache only the pieces that are difficult to produce, or you can cache your entire site.
from django.core.wsgi import get_wsgi_application
from django.http import HttpResponse, HttpResponseBadRequest

from io import BytesIO      # BytesIO is a libary for working with IO streams, in this case we're using this creating some binary data
from PIL import Image, ImageDraw

class ImageForm(forms.Form):
    ''' Width and Height value is taken from the URL, and is put into a form to make use of in-built validation features '''
    height = forms.IntegerField(min_value=1, max_value=2000)
    width = forms.IntegerField(min_value=1, max_value=2000)

    def generate(self, image_format='PNG'):     # Forms can have custom methods
        """Generate an image of the given type and return as raw bytes."""
        height = self.cleaned_data['height']        # once the form is created, we'll have access to this method and the cleaned_data object
        width = self.cleaned_data['width']
        key = '{}.{}.{}'.format(width, height, image_format)        # generate a cache key, depending on the width, height and image_format. That way if we get the same request over and over, we don't generate the new image each time 
        content = cache.get(key)

        content = cache.get(key)                                    # either return None or return the content based on when it was generated last time 
        if content is None:                                         # see if this content exists. If None, this is called a cache-miss, and therefore we want to perform this labour intensive work. 
            image = Image.new('RGB', (width, height))       # Pillow is a library for opening, manipulating, and saving many different image file formats.
            draw = ImageDraw.Draw(image)
            text = '{} X {}'.format(width, height)
            textwidth, textheight = draw.textsize(text)

            if textwidth < width and textheight < height:
                texttop = (height - textheight) // 2
                textleft = (width - textwidth) // 2
                draw.text((textleft, texttop), text, fill=(255, 255, 255))      

            content = BytesIO()                             # create a new binary stream
            image.save(content, image_format)
            content.seek(0)                                 # SEEK_SET or 0 – start of the stream (the default); offset should be zero or positive. Not 100% sure on this one, perhaps it's for resetting the stream back to zero before returning it as an object?                          
            cache.set(key, content, 60 * 60)                # cache this content for future use 
        return content    

def placeholder(request, width, height):
    form = ImageForm({'height': height, 'width': width})        # place this into the form so as to start the validation process 
    if form.is_valid():
        image = form.generate()
        return HttpResponse(image, content_type='image/png')
    else:                                                       # returns HTTP code 400 (bad request) if form.is_valid returns False
        return HttpResponseBadRequest('Invalid Image Request')

def index(request):
    return HttpResponse('Hello World')

urlpatterns = (
    url(r'^image/(?P<width>[0-9]+)x(?P<height>[0-9]+)/$', placeholder, name='placeholder'),
    url(r'^$', index, name='homepage'),
)

application = get_wsgi_application()

if __name__ == "__main__":
    from django.core.management import execute_from_command_line
    
    execute_from_command_line(sys.argv)