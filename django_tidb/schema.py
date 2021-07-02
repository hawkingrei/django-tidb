from django.db.backends.mysql import base as mysql_base
from django.db.models import NOT_PROVIDED


class DatabaseSchemaEditor(mysql_base.DatabaseSchemaEditor):
    @property
    def sql_delete_check(self):
        return 'ALTER TABLE %(table)s DROP CHECK %(name)s'

    @property
    def sql_rename_column(self):
        return 'ALTER TABLE %(table)s CHANGE %(old_column)s %(new_column)s %(type)s'

    def quote_value(self, value):
        self.connection.ensure_connection()
        if isinstance(value, str):
            value = value.replace('%', '%%')
        # MySQLdb escapes to string, PyMySQL to bytes.
        quoted = self.connection.connection.escape(value, self.connection.connection.encoders)
        if isinstance(value, str) and isinstance(quoted, bytes):
            quoted = quoted.decode()
        return quoted

    def _is_limited_data_type(self, field):
        db_type = field.db_type(self.connection)
        return db_type is not None and db_type.lower() in self.connection._limited_data_types

    def skip_default(self, field):
        if not self._supports_limited_data_type_defaults:
            return self._is_limited_data_type(field)
        return False

    @property
    def _supports_limited_data_type_defaults(self):
        # MariaDB >= 10.2.1 and MySQL >= 8.0.13 supports defaults for BLOB
        # and TEXT.
        return True

    def _column_default_sql(self, field):
        if (
            self._supports_limited_data_type_defaults and
            self._is_limited_data_type(field)
        ):
            # MySQL supports defaults for BLOB and TEXT columns only if the
            # default value is written as an expression i.e. in parentheses.
            return '(%s)'
        return super()._column_default_sql(field)

    def add_field(self, model, field):
        super().add_field(model, field)

        # Simulate the effect of a one-off default.
        # field.default may be unhashable, so a set isn't used for "in" check.
        if self.skip_default(field) and field.default not in (None, NOT_PROVIDED):
            effective_default = self.effective_default(field)
            self.execute('UPDATE %(table)s SET %(column)s = %%s' % {
                'table': self.quote_name(model._meta.db_table),
                'column': self.quote_name(field.column),
            }, [effective_default])

    def _field_should_be_indexed(self, model, field):
        create_index = super()._field_should_be_indexed(model, field)
        storage = self.connection.introspection.get_storage_engine(
            self.connection.cursor(), model._meta.db_table
        )
        # No need to create an index for ForeignKey fields except if
        # db_constraint=False because the index from that constraint won't be
        # created.
        if (storage == "InnoDB" and
                create_index and
                field.get_internal_type() == 'ForeignKey' and
                field.db_constraint):
            return False
        return not self._is_limited_data_type(field) and create_index

    def _delete_composed_index(self, model, fields, *args):
        """
        MySQL can remove an implicit FK index on a field when that field is
        covered by another index like a unique_together. "covered" here means
        that the more complex index starts like the simpler one.
        http://bugs.mysql.com/bug.php?id=37910 / Django ticket #24757
        We check here before removing the [unique|index]_together if we have to
        recreate a FK index.
        """
        first_field = model._meta.get_field(fields[0])
        if first_field.get_internal_type() == 'ForeignKey':
            constraint_names = self._constraint_names(model, [first_field.column], index=True)
            if not constraint_names:
                self.execute(
                    self._create_index_sql(model, fields=[first_field], suffix='')
                )
        return super()._delete_composed_index(model, fields, *args)

    def _set_field_new_type_null_status(self, field, new_type):
        """
        Keep the null property of the old field. If it has changed, it will be
        handled separately.
        """
        if field.null:
            new_type += " NULL"
        else:
            new_type += " NOT NULL"
        return new_type

    def _alter_column_type_sql(self, model, old_field, new_field, new_type):
        new_type = self._set_field_new_type_null_status(old_field, new_type)
        return super()._alter_column_type_sql(model, old_field, new_field, new_type)

    def _rename_field_sql(self, table, old_field, new_field, new_type):
        new_type = self._set_field_new_type_null_status(old_field, new_type)
        return super()._rename_field_sql(table, old_field, new_field, new_type)
