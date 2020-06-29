from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def url_replace(context, next_page):
    query = context['request'].GET.copy().urlencode()
    if (not query):
        return f'page={next_page}' #creates page= query
    else:
        if ('page=' in query) and ('&page=' not in query): #when page= is in query, but there are no other queries
            return f'page={next_page}'
        elif '&page=' in query: # page and other queries exist
            url = query.rpartition('&page=')[0]  # equivalent to .split('page='), except more efficient
            return f'{url}&page={next_page}'
        else: #add &page=
            url = query
            return f'{url}&page={next_page}'