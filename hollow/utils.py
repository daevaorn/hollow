from copy import copy

class Cloneable(object):
    r"""
        >>> class Foo(Cloneable):
        ...     fields_to_clone = ['a', 'b', 'c']
        ...
        ...     def __init__(self, a, b, c):
        ...         self.a = a
        ...         self.b = b
        ...         self.c = c
        ...
        ...     def clone_c(self, old_value, new_value):
        ...         old_value.update(new_value)
        ...         return old_value
        ...
        ...     def __repr__(self):
        ...         return '<%s, %s, %s>' % (self.a, self.b, self.c)

        >>> f = Foo(1, [2], {3: 3})
        >>> f
        <1, [2], {3: 3}>
        >>> f.clone(a=4)
        <4, [2], {3: 3}>
        >>> f.clone(b=[4])
        <1, [4], {3: 3}>
        >>> f.clone(c={4: 4})
        <1, [2], {3: 3, 4: 4}>
    """

    fields_to_clone = []

    def clone(self, **kwargs):
        defaults = dict((field, copy(getattr(self, field, None)))\
                                    for field in self.fields_to_clone)

        for name, value in kwargs.iteritems():
            if name not in defaults:
                continue

            if hasattr(self, 'clone_%s' % name):
                defaults[name] = getattr(self, 'clone_%s' % name)(defaults[name], value)
            else:
                defaults[name] = value

        return self.create_clone(**defaults)

    def create_clone(self, **defaults):
        return self.__class__(**defaults)


def patch_log_entry_model():
    from django.contrib.admin.models import LogEntry

    return_self = lambda self, *args, **kwargs: self

    class LogEntryManager(object):
        __iter__ = lambda self: iter([])
        __getitem__ = return_self
        filter = return_self
        select_related = return_self

    LogEntry.objects = LogEntryManager()
