"""
MySQL database backend for Django.
Requires mysqlclient: https://pypi.org/project/mysqlclient/
"""
from django.db.backends.mysql.base import (
    DatabaseWrapper as MysqlDatabaseWrapper,
)
from django.utils.functional import cached_property

# Some of these import MySQLdb, so import them after checking if it's installed.
from .features import DatabaseFeatures
from .introspection import DatabaseIntrospection
from .operations import DatabaseOperations
from .schema import DatabaseSchemaEditor
from .version import TiDBVersion

server_version = TiDBVersion()

class DatabaseWrapper(MysqlDatabaseWrapper):
    vendor = 'tidb'
    display_name = 'TiDB'

    SchemaEditorClass = DatabaseSchemaEditor
    # Classes instantiated in __init__().
    features_class = DatabaseFeatures
    introspection_class = DatabaseIntrospection
    ops_class = DatabaseOperations

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
                       CONVERT_TZ('2001-01-01 01:00:00', 'UTC', 'UTC') IS NOT NULL,
                       @@session.time_zone
            """)
            row = cursor.fetchone()
        return {
            'version': row[0],
            'sql_mode': row[1],
            'default_storage_engine': row[2],
            'sql_auto_is_null': bool(row[3]),
            'lower_case_table_names': bool(row[4]),
            'has_zoneinfo_database': bool(row[5]),
            'timezone': row[6],
        }

    @cached_property
    def tidb_server_info(self):
        return self.tidb_server_data['version']

    @cached_property
    def tidb_version(self):
        match = server_version.match(self.tidb_server_info)
        if not match:
            raise Exception('Unable to determine Tidb version from version string %r' % self.tidb_server_info)
        return server_version.version

    @cached_property
    def sql_mode(self):
        sql_mode = self.tidb_server_data['sql_mode']
        return set(sql_mode.split(',') if sql_mode else ())

    def ensure_timezone(self):
        if self.connection is None:
            return False
        conn_timezone_name = self.tidb_server_data['timezone']
        timezone_name = self.timezone_name
        if timezone_name and conn_timezone_name != timezone_name:
            with self.cursor() as cursor:
                cursor.execute(self.ops.set_time_zone_sql(), [timezone_name])
            return True
        return False

    def init_connection_state(self):
        assignments = []
        timezone_changed = self.ensure_timezone()
        if timezone_changed:
            # Commit after setting the time zone (see #17062)
            if not self.get_autocommit():
                self.connection.commit()
        if self.features.is_sql_auto_is_null_enabled:
            # SQL_AUTO_IS_NULL controls whether an AUTO_INCREMENT column on
            # a recently inserted row will return when the field is tested
            # for NULL. Disabling this brings this aspect of MySQL in line
            # with SQL standards.
            assignments.append('SET SQL_AUTO_IS_NULL = 0')

        if self.isolation_level:
            assignments.append('SET SESSION TRANSACTION ISOLATION LEVEL %s' % self.isolation_level.upper())

        if assignments:
            with self.cursor() as cursor:
                cursor.execute('; '.join(assignments))
