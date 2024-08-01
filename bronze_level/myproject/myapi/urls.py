# myapi/urls.py
from django.urls import path
from .views import RunScriptView
from .views import RunSQLQueryView, RunSQLQueryOnly3, RunSQLQueryView2

# urlpatterns = [
#     path('run-sql-query/', RunSQLQueryView.as_view(), name='run-sql-query'),
# ]


urlpatterns = [
    path('run-script/', RunScriptView.as_view(), name='run-script'),
    path('run-sql-query/', RunSQLQueryView.as_view(), name='run-sql-query'),
    path('run-sqlonly3/', RunSQLQueryOnly3.as_view(), name='run-sql-query-only'),
    path('run-sql-main/', RunSQLQueryView2.as_view(), name='run-sql-query-only'),
]
