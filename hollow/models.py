# -*- coding: utf-8 -*-
from django.db.models.base import ModelState
from django.db.models.fields import FieldDoesNotExist
from django.utils.datastructures import SortedDict

from hollow.fields import Field

class Meta(object):
    auto_created = False

    abstract = False
    db_table = None

    local_many_to_many = []
    many_to_many = local_many_to_many

    unique_together = []

    parents = {}

    proxy = None

    managed = False

    pk = Field('pk', unique=True, primary_key=True, auto_created=True, editable=False)

    def __init__(self, model_name, app_label, fields, verbose_name,
                 verbose_name_plural, ordering=None):
        self.object_name = self.model_name = model_name
        self.module_name = self.model_name.lower()
        self.app_label = app_label

        self.verbose_name_raw = self.verbose_name = verbose_name
        self.verbose_name_plural = verbose_name_plural

        self.fields_dict = SortedDict(
            [('pk', self.pk)] + [(f, Field(f)) for f in fields]
        )

        self.has_auto_field = True
        self.auto_field = self.pk

        self.fields = self.local_fields = self.fields_dict.values()

        self.ordering = ordering

    def get_field(self, name):
        if name not in self.fields_dict:
            raise FieldDoesNotExist('No field `%s` in model: %s' % (name, self.object_name))
        return self.fields_dict[name]

    def get_field_by_name(self, name):
        return (self.get_field(name), None, True)

    def get_ordered_objects(self):
        return []

    def get_all_related_objects(self, include_hidden=None):
        return []

    def get_all_related_many_to_many_objects(self):
        return []

    def get_delete_permission(self):
        return 'delete'

class Model(object):
    _deferred = False
    _state = ModelState()

    class DoesNotExist(Exception):
        pass

    def __init__(self, *args, **kwargs):
        if self.adapter.fields_defaults:
            self.__dict__.update(self.adapter.fields_defaults)

        for i, arg in enumerate(args):
            field_name = self.adapter.fields[i]

            setattr(self, field_name, arg)

        self.__dict__.update(kwargs)

        keys = set(self.__dict__.keys())
        for name in self.adapter.fields:
            if name not in keys:
                setattr(self, name, None)

    def __unicode__(self):
        return self.adapter.to_unicode(self)

    def save(self):
        self.adapter.put(self)

    def delete(self):
        self.adapter.delete(self)

    def _get_pk_val(self):
        if not getattr(self, '_pk_cache', None):
            self._pk_cache = self.adapter.id(self)
        return self._pk_cache
    def _set_pk_val(self, val):
        self._pk_cache = val
    pk = property(_get_pk_val, _set_pk_val)

    def serializable_value(self, field_name):
        getattr(self, field_name)

    def clean_fields(self, exclude=None):
        pass

    def clean(self):
        pass

    def _get_unique_checks(self, exclude=None):
        return [], []

    def validate_unique(self, exclude=None):
        pass

    def _collect_sub_objects(self, collector):
        pass
