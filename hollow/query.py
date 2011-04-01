# -*- coding: utf-8 -*-
from django.db.models import query_utils

from hollow.utils import Cloneable

class Query(Cloneable):
    select_related = True # чтобы админка не пыталась сама применить select_related

    fileds_to_clone = ['flat', 'as_dict']

    def __init__(self, flat=None, as_dict=None):
        self.flat = flat
        self.as_dict = as_dict

    @property
    def where(self):
        return None

class QuerySet(object):
    query_class = Query
    db = 'default'

    def __init__(self, model, query=None, params=None):
        self.model = model
        self.adapter = model.adapter

        self.query = query or self.query_class()
        self.params = params or self.adapter.params_class()

        self._results_cache = None

    def __iter__(self):
        if not self._results_cache:
            if self.params.values:
                process = lambda row: dict(zip(self.params.values, row))
            elif self.query.flat:
                process = lambda row: row[0]
            else:
                process = lambda row: row

            self._results_cache = map(process, self._adapter_get())

        for row in self._results_cache:
            yield row

    def __len__(self):
        return len(list(self.__iter__()))

    @property
    def ordered(self):
        return bool(self.params.order_by)

    def count(self):
        return self.adapter.count(self.params.clone())

    def __getitem__(self, key):
        if isinstance(key, slice):
            data = {}
            if key.start is not None:
                data['offset'] = key.start
            if key.stop is not None:
                if slice.start:
                    data['limit'] = key.stop - key.start
                else:
                    data['limit'] = key.stop
        else:
            data = {
                'offset': key,
                'limit': 1
            }
            return list(self._clone(**data))[0]

        return self._clone(**data)

    def all(self):
        return self.get_query_set()

    def filter(self, *args, **kwargs):
        if args and issubclass(type(args[0]), query_utils.Q):
            q = args[0]
            new_kwargs = {}
            new_kwargs.update(kwargs)
            new_kwargs.update(dict(q.children))
            return self._clone(filters=new_kwargs)
        return self._clone(filters=kwargs)

    def order_by(self, *args):
        return self._clone(order_by=args)

    def distinct(self):
        return self._clone(distinct=True)

    def values(self, *fields):
        return self._clone(values=fields, as_dict=True)

    def values_list(self, *fields, **kwargs):
        return self._clone(fields=fields, flat=kwargs.get('flat', False))

    def get(self, *args, **kwargs):
        try:
            return self._clone(filters=kwargs)[0]
        except IndexError:
            raise self.model.DoesNotExist(u'Lookup: %s' % self.params.__dict__)

    def create(self, **kwargs):
        instance = self.model(**kwargs)
        self.adapter.put(instance)

        return instance

    def get_or_create(self, **kwargs):
        defaults = kwargs.pop('defaults', {})
        try:
            return self.get(**kwargs), False
        except self.model.DoesNotExist:
            kwargs.update(defaults)
            return self.create(**kwargs), True

    def get_query_set(self):
        return self._clone()

    def using(self, db):
        return self._clone()

    def _clone(self, **kwargs):
        return self.__class__(
            self.model,
            self.query.clone(**kwargs),
            self.params.clone(**kwargs),
        )

    def _adapter_get(self):
        return self.adapter.get(self.params.clone())

    def delete(self, *args, **kwargs):
        for obj in self:
            obj.delete()
