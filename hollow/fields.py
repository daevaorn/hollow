from django import forms

class Field(object):
    rel = None
    blank = True
    flatchoices = []
    choices = []

    db_index = None

    def __init__(self, name, verbose_name=None, editable=True, unique=False,
                auto_created=False, primary_key=False):
        self.name = name
        self.attname = name
        self.verbose_name = verbose_name or name
        self.editable = editable
        self.unique = unique
        self.auto_created = auto_created
        self.primary_key = primary_key

    def formfield(self, **kwargs):
        return forms.Field()

    def get_db_prep_lookup(self, lookup_type, value, connection, prepared=False):
        return [value]

    def value_from_object(self, instance):
        return getattr(instance, self.name)

    def save_form_data(self, instance, value):
        setattr(instance, self.name, value)

    def to_python(self, value):
        return value

    def __repr__(self):
        return '<hollow.Field: %s>' % self.name

class M2MRelation(object):
    def __init__(self, to=None, limit_choices_to={}):
        self.to = to
        self.limit_choices_to = limit_choices_to
