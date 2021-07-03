import uuid

from django.conf import settings
from django.db.backends.base.operations import BaseDatabaseOperations
from django.utils import timezone
from django.utils.encoding import force_str
from django.db.backends.mysql.operations import (
    DatabaseOperations as MysqlDatabaseOperations,
)

class DatabaseOperations(MysqlDatabaseOperations):
    def explain_query_prefix(self, format=None, **options):
        # Alias MySQL's TRADITIONAL to TEXT for consistency with other backends.
        if format and format.upper() == 'TEXT':
            format = 'TRADITIONAL'
        elif not format and 'TREE' in self.connection.features.supported_explain_formats:
            # Use TREE by default (if supported) as it's more informative.
            format = 'TREE'
        analyze = options.pop('analyze', False)
        prefix = super().explain_query_prefix(format, **options)
        if analyze:
            # MariaDB uses ANALYZE instead of EXPLAIN ANALYZE.
            prefix = 'ANALYZE' if self.connection.mysql_is_mariadb else prefix + ' ANALYZE'
        return prefix

    def regex_lookup(self, lookup_type):
        # REGEXP BINARY doesn't work correctly in MySQL 8+ and REGEXP_LIKE
        # doesn't exist in MySQL 5.x or in MariaDB.
        if lookup_type == 'regex':
            return '%s REGEXP BINARY %s'
        return '%s REGEXP %s'

    def lookup_cast(self, lookup_type, internal_type=None):
        lookup = '%s'
        if internal_type == 'JSONField':
            lookup = 'JSON_UNQUOTE(%s)'
        return lookup
