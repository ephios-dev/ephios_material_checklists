import math

from django import template

register = template.Library()


@register.filter(name='chunks')
def chunks(iterable, chunk_amount):
    # Return iterable
    if not hasattr(iterable, '__iter__') or not iterable:
        return iterable

    # Determine chunk size and initialize counters
    chunk_size = math.ceil(len(iterable)/chunk_amount)
    yielded_chunks = 0
    iterated_items = 0
    chunk = []

    # Iterate items
    for item in iterable:
        chunk.append(item)
        iterated_items += 1
        # Yield chunk when enough items where iterated and reset chunk
        if not iterated_items % chunk_size:
            yielded_chunks += 1
            yield chunk
            chunk = []

    # Yield remaining chunks (including empty ones)
    while yielded_chunks < chunk_amount:
        yielded_chunks += 1
        yield chunk