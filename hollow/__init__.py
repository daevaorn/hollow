from django.contrib.admin.models import LogEntry

from hollow import admin

return_self = lambda self, *args, **kwargs: self

class LogEntryManager(object):
    __iter__ = lambda self: iter([])
    __getitem__ = return_self
    filter = return_self
    select_related = return_self

def patch_log_entry_model():
    LogEntry.objects = LogEntryManager()

patch_log_entry_model()
