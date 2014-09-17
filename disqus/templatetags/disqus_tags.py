from django import template
from django.conf import settings

register = template.Library()

# Set the disqus_identifier variable to some unique value. Defaults to
# page's URL
@register.simple_tag(takes_context=True)
def set_disqus_identifier(context, *args):
    '''
    Set the disqus_identifier variable to some unique value. Defaults to
    page's URL.
    '''
    context['disqus_identifier'] = "".join(args)
    return ""

@register.simple_tag(takes_context=True)
def set_disqus_url(context, *args):
    '''
    Set the disqus_url variable to some value. Defaults to page's
    location.
    '''
    context['disqus_url'] = "".join(args)
    return ""

@register.simple_tag(takes_context=True)
def set_disqus_title(context, disqus_title):
    '''
    Set the disqus_title variable to some value. Defaults to page's
    title or URL.
    '''
    context['disqus_title'] = disqus_title
    return ""

@register.simple_tag(takes_context=True)
def set_disqus_category_id(context, disqus_category_id):
    '''
    Set the disqus_category_id variable to some value. No default. See
    http://help.disqus.com/customer/portal/articles/472098-javascript-configuration-variables#disqus_category_id
    '''
    context['disqus_category_id'] = disqus_category_id
    return ""

def get_config(context):
    """
    return the formatted javascript for any disqus config variables
    """
    conf_vars = ['disqus_developer', 'disqus_identifier', 'disqus_url',
                 'disqus_title', 'disqus_category_id']

    output = []
    for item in conf_vars:
        if item in context:
            output.append('\tvar %s = "%s";' % (item, context[item]))
    return '\n'.join(output)

@register.inclusion_tag('disqus/recent_comments.html',
                        takes_context=True)
def disqus_recent_comments(context, shortname='', num_items=5,
                           excerpt_length=200, hide_avatars=0,
                           avatar_size=32):
    """
    Return the HTML/js code which shows recent comments.

    """
    shortname = getattr(settings, 'DISQUS_WEBSITE_SHORTNAME', shortname)
    return {
        'shortname': shortname,
        'num_items': num_items,
        'hide_avatars': hide_avatars,
        'avatar_size': avatar_size,
        'excerpt_length': excerpt_length,
        'config': get_config(context),
    }

@register.inclusion_tag('disqus/show_comments.html', takes_context=True)
def disqus_show_comments(context, shortname=''):
    """
    Return the HTML code to display DISQUS comments.
    """
    shortname = getattr(settings, 'DISQUS_WEBSITE_SHORTNAME', shortname)
    return {
        'shortname': shortname,
        'config': get_config(context),
    }
