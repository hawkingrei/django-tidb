"""
MySQL database backend for Django.
Requires mysqlclient: https://pypi.org/project/mysqlclient/
"""
from django.core.exceptions import ImproperlyConfigured
from django.db import IntegrityError
from django.db.backends import utils as backend_utils
from django.db.backends.base.base import BaseDatabaseWrapper
from django.utils.asyncio import async_unsafe
from django.utils.functional import cached_property
from django.utils.regex_helper import _lazy_re_compile

from django.db.backends import mysql

# Some of these import MySQLdb, so import them after checking if it's installed.
from .client import DatabaseClient
from .creation import DatabaseCreation
from .features import DatabaseFeatures
from .introspection import DatabaseIntrospection
from .operations import DatabaseOperations
from .schema import DatabaseSchemaEditor
from .validation import DatabaseValidation

version = Database.version_info
if version < (1, 4, 0):
    raise ImproperlyConfigured('mysqlclient 1.4.0 or newer is required; you have %s.' % Database.__version__)


# MySQLdb returns TIME columns as timedelta -- they are more like timedelta in
# terms of actual behavior as they are signed and include days -- and Django
# expects time.
django_conversions = {
    **conversions,
    **{FIELD_TYPE.TIME: backend_utils.typecast_time},
}

# This should match the numerical portion of the version numbers (we can treat
# versions like 5.0.24 and 5.0.24a as the same).
server_version_re = _lazy_re_compile(r'(\d{1,2})\.(\d{1,2})\.(\d{1,2})')


class CursorWrapper:
    """
    A thin wrapper around MySQLdb's normal cursor class that catches particular
    exception instances and reraises them with the correct types.
    Implemented as a wrapper, rather than a subclass, so that it isn't stuck
    to the particular underlying representation returned by Connection.cursor().
    """
    codes_for_integrityerror = (
        1048,  # Column cannot be null
        1690,  # BIGINT UNSIGNED value is out of range
        3819,  # CHECK constraint is violated
        4025,  # CHECK constraint failed
    )

    def __init__(self, cursor):
        self.cursor = cursor

    def execute(self, query, args=None):
        try:
            # args is None means no string interpolation
            return self.cursor.execute(query, args)
        except Database.OperationalError as e:
            # Map some error codes to IntegrityError, since they seem to be
            # misclassified and Django would prefer the more logical place.
            if e.args[0] in self.codes_for_integrityerror:
                raise IntegrityError(*tuple(e.args))
            raise

    def executemany(self, query, args):
        try:
            return self.cursor.executemany(query, args)
        except Database.OperationalError as e:
            # Map some error codes to IntegrityError, since they seem to be
            # misclassified and Django would prefer the more logical place.
            if e.args[0] in self.codes_for_integrityerror:
                raise IntegrityError(*tuple(e.args))
            raise

    def __getattr__(self, attr):
        return getattr(self.cursor, attr)

    def __iter__(self):
        return iter(self.cursor)


class DatabaseWrapper(mysql.DatabaseWrapper):
    vendor = 'tidb'

    SchemaEditorClass = DatabaseSchemaEditor
    # Classes instantiated in __init__().
    client_class = DatabaseClient
    creation_class = DatabaseCreation
    features_class = DatabaseFeatures
    introspection_class = DatabaseIntrospection
    ops_class = DatabaseOperations
    validation_class = mysql.DatabaseValidation

    @cached_property
    def display_name(self):
        return 'TiDB'

    @cached_property
    def data_type_check_constraints(self):
        if self.features.supports_column_check_constraints:
            check_constraints = {'PositiveBigIntegerField': '`%(column)s` >= 0',
                                 'PositiveIntegerField': '`%(column)s` >= 0',
                                 'PositiveSmallIntegerField': '`%(column)s` >= 0',
                                 'JSONField': 'JSON_VALID(`%(column)s`)'}
            # MariaDB < 10.4.3 doesn't automatically use the JSON_VALID as
            # a check constraint.
            return check_constraints
        return {}

    @cached_property
    def tidb_server_data(self):
        with self.temporary_connection() as cursor:
            # Select some server variables and test if the time zone
            # definitions are installed. CONVERT_TZ returns NULL if 'UTC'
            # timezone isn't loaded into the mysql.time_zone table.
            cursor.execute("""
                SELECT VERSION(),
                       @@sql_mode,
                       @@default_storage_engine,
                       @@sql_auto_is_null,
                       @@lower_case_table_names,
                       CONVERT_TZ('2001-01-01 01:00:00', 'UTC', 'UTC') IS NOT NULL
            """)
            row = cursor.fetchone()
        return {
            'version': row[0],
            'sql_mode': row[1],
            'default_storage_engine': row[2],
            'sql_auto_is_null': bool(row[3]),
            'lower_case_table_names': bool(row[4]),
            'has_zoneinfo_database': bool(row[5]),
        }

    @cached_property
    def tidb_server_info(self):
        return self.tidb_server_data['version']

    @cached_property
    def tidb_version(self):
        match = server_version_re.match(self.tidb_server_info)
        if not match:
            raise Exception('Unable to determine Tidb version from version string %r' % self.tidb_server_info)
        return tuple(int(x) for x in match.groups())

    @cached_property
    def sql_mode(self):
        sql_mode = self.tidb_server_data['sql_mode']
        return set(sql_mode.split(',') if sql_mode else ())
