# -*- coding: utf-8 -*-
from django.db.models import loading
from django.contrib.contenttypes.models import ContentType
from django.utils.datastructures import MultiValueDict

from hollow.models import Model, Meta
from hollow.query import QuerySet
from hollow.utils import Cloneable

class FakeContentType(object):
    def __init__(self, id, model):
        self.id = self.pk = id
        self.model = model

    def model_class(self):
        return self.model

class AdapterMeta(type):
    popup_fields = ['app_label', 'model_name', 'fields', 'model_prototype',
                    'model_verbose_name', 'model_verbose_name_plural',
                    'queryset_class']

    def __new__(cls, name, bases, attrs_override):
        try:
            Adapter
        except NameError:
            return super(AdapterMeta, cls).__new__(cls, name, bases, attrs_override)

        attrs = dict((field, getattr(base, field))
                     for field in cls.popup_fields
                     for base in bases)
        attrs.update({'abstract': False})
        attrs.update(attrs_override)

        if not attrs['abstract']:
            model_prototype = attrs['model_prototype']

            model_name = attrs['model_name'] or model_prototype.__name__
            model = attrs['model'] = type(model_name, (model_prototype,), {})

            adapter_class = super(AdapterMeta, cls).__new__(cls, name, bases, attrs)

            adapter = model.adapter = adapter_class()

            model._meta = Meta(
                model_name=model.__name__,
                app_label=adapter.app_label,
                fields=adapter.fields,
                verbose_name=adapter.model_verbose_name,
                verbose_name_plural=adapter.model_verbose_name_plural,
            )
            model._default_manager = model.objects = attrs['queryset_class'](model)

            if hasattr(model, 'class_prepared'):
                model.class_prepared()

            loading.cache.register_models(adapter.app_label, model)
            ContentType.objects._add_to_cache(
                'default', # база
                FakeContentType(
                    '%s.%s' % (adapter.app_label, model._meta.object_name),
                    model
                )
            )

            return adapter_class
        else:
            return super(AdapterMeta, cls).__new__(cls, name, bases, attrs)


class Params(Cloneable):
    fields_to_clone = ['filters', 'order_by', 'offset', 'limit', 'distinct', 'values']

    def __init__(self, filters=None, order_by=None, offset=None, limit=None,
                distinct=None, values=None, keys_in=False):
        self.filters = filters or MultiValueDict()
        self.order_by = order_by or []
        self.offset = offset
        self.limit = limit
        self.distinct = distinct
        self.values = values or []
        self.keys_in = 'pk__in' in self.filters or keys_in

    def get_slice(self):
        offset = self.offset
        limit = self.limit
        if offset is not None and limit is not None:
            limit = offset + limit
        return slice(offset, limit)

    def clone_filters(self, value, new_value):
        value.update(new_value)
        return value

    def __repr__(self):
        return '<Params: %s>' % repr(self.__dict__)


class Adapter(object):
    __metaclass__ = AdapterMeta

    queryset_class = QuerySet

    app_label = None
    model_name = None

    model_prototype = Model

    fields = None
    fields_defaults = None

    model_verbose_name = None
    model_verbose_name_plural = None

    abstract = True

    params_class = Params

    def get(self, params):
        raise NotImplementedError

    def count(self, params):
        raise NotImplementedError

    def put(self, instance):
        raise NotImplementedError

    def delete(self, instance):
        raise NotImplementedError

    def id(self, instance):
        raise NotImplementedError

    def to_unicode(self, instance):
        raise NotImplementedError

    def _collect_sub_objects(self, collector):
        raise NotImplementedError
