# -*- coding: utf-8 -*-
from django import forms
from django.utils.encoding import force_unicode

from hollow.adapter import Adapter
from hollow.admin import AdminSite, ModelAdmin

class PostAdapter(Adapter):
    app_label = 'hollow'

    model_name = 'Post'

    model_verbose_name = 'post'
    model_verbose_name_plural = 'posts'

    fields = ['title', 'text', 'status']

    def get(self, *args, **kwargs):
        return [self.model('test post', 'test text', 'published')]

    def count(self, *args, **kwargs):
        return 1

    def id(self, instance):
        return getattr(instance, 'id', None)

    def to_unicode(self, instance):
        return force_unicode(instance._doc)

    def put(self, instance):
        pass

    def delete(self, instance):
        pass

class PostAdminForm(forms.ModelForm):
    class Meta:
        model = PostAdapter.model
        fields = ['title', 'text', 'status']

    name = forms.CharField()
    description = forms.CharField(widget=forms.Textarea)

class PostAdmin(ModelAdmin):
    form = PostAdminForm
    list_display = ('title', 'status')

site = AdminSite()

site.register([PostAdapter.model], PostAdmin)
