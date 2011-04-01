from django.db.backends.dummy.base import *
from django.db.backends.dummy.base import DatabaseWrapper as DummyDatabaseWrapper

class DatabaseWrapper(DummyDatabaseWrapper):
    def _enter_transaction_management(self, *args, **kwargs):
        pass

    def _leave_transaction_management(self, *args, **kwargs):
        pass
