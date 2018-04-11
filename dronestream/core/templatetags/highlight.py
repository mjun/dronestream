from django import template

register = template.Library()


@register.filter
def highlight(text, terms):
    start_tag = '<span class="highlighted">'
    end_tag = '</span>'

    if terms:
        if isinstance(terms, str):
            terms = [terms]

        if isinstance(terms, list):
            for term in terms:
                found_at_index = text.lower().find(term.lower())
                while found_at_index > -1:
                    text = text[:found_at_index] + start_tag + text[found_at_index:]
                    text = text[:found_at_index + len(start_tag) + len(term)] + end_tag + text[found_at_index + len(
                        start_tag) + len(term):]
                    offset = found_at_index + len(start_tag) + len(end_tag)
                    found_at_index = text.lower().find(term.lower(), offset)
    return text
