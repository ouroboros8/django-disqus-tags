import urllib
import json

from django.core.management.base import CommandError
from django.conf import settings

def call(method, data, post=False):
    """
    Calls `method` from the DISQUS API with data either in POST or GET.
    Returns deserialized JSON response.
    """
    url = "%s%s" % ('http://disqus.com/api/', method)
    if post:
        # POST request
        url += "/"
        data = urllib.parse.urlencode(data)
    else:
        # GET request
        url += "?%s" % urllib.parse.urlencode(data)
        data = ''
    res = json.load(urllib.request.urlopen(url, data))
    if not res['succeeded']:
        raise CommandError("'%s' failed: %s\nData: %s" % (method, res['code'], data))
    return res['message']
