from django.db.backends.mysql.schema import (
    DatabaseSchemaEditor as MysqlDatabaseSchemaEditor,
)

class DatabaseSchemaEditor(MysqlDatabaseSchemaEditor):
    @property
    def sql_delete_check(self):
        return 'ALTER TABLE %(table)s DROP CHECK %(name)s'

    @property
    def sql_rename_column(self):
        return 'ALTER TABLE %(table)s CHANGE %(old_column)s %(new_column)s %(type)s'

    def skip_default_on_alter(self, field):
        return False

    @property
    def _supports_limited_data_type_defaults(self):
        # MariaDB >= 10.2.1 and MySQL >= 8.0.13 supports defaults for BLOB
        # and TEXT.
        return True

    def _field_should_be_indexed(self, model, field):
        return False
