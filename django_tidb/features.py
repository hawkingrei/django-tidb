
import operator

from django.db.backends.base.features import BaseDatabaseFeatures
from django.utils.functional import cached_property


class DatabaseFeatures(BaseDatabaseFeatures):
    empty_fetchmany_value = ()
    allows_group_by_pk = True
    uses_savepoints = True
    related_fields_match_type = True
    # MySQL doesn't support sliced subqueries with IN/ALL/ANY/SOME.
    allow_sliced_subqueries_with_in = False
    has_select_for_update = True
    supports_forward_references = False
    supports_regex_backreferencing = False
    supports_date_lookup_using_string = False
    supports_timezones = False
    requires_explicit_null_ordering_when_grouping = True
    can_release_savepoints = True
    atomic_transactions = False
    can_clone_databases = True
    supports_temporal_subtraction = True
    supports_select_intersection = False
    supports_select_difference = False
    supports_slicing_ordering_in_compound = True
    supports_index_on_text_field = False
    has_case_insensitive_like = False
    create_test_procedure_without_params_sql = """
        CREATE PROCEDURE test_procedure ()
        BEGIN
            DECLARE V_I INTEGER;
            SET V_I = 1;
        END;
    """
    create_test_procedure_with_int_param_sql = """
        CREATE PROCEDURE test_procedure (P_I INTEGER)
        BEGIN
            DECLARE V_I INTEGER;
            SET V_I = P_I;
        END;
    """
    # Neither MySQL nor MariaDB support partial indexes.
    supports_partial_indexes = False
    # COLLATE must be wrapped in parentheses because MySQL treats COLLATE as an
    # indexed expression.
    collate_as_index_expression = True

    supports_order_by_nulls_modifier = False
    order_by_nulls_first = True
    test_collations = {
        'ci': 'utf8_general_ci',
        'non_default': 'utf8_esperanto_ci',
        'swedish_ci': 'utf8_swedish_ci',
    }

    @cached_property
    def django_test_skips(self):
        skips = {
            "This doesn't work on MySQL.": {
                'db_functions.comparison.test_greatest.GreatestTests.test_coalesce_workaround',
                'db_functions.comparison.test_least.LeastTests.test_coalesce_workaround',
            },
            'Running on MySQL requires utf8mb4 encoding (#18392).': {
                'model_fields.test_textfield.TextFieldTests.test_emoji',
                'model_fields.test_charfield.TestCharField.test_emoji',
            },
            "MySQL doesn't support functional indexes on a function that "
            "returns JSON": {
                'schema.tests.SchemaTests.test_func_index_json_key_transform',
            },
            "MySQL supports multiplying and dividing DurationFields by a "
            "scalar value but it's not implemented (#25287).": {
                'expressions.tests.FTimeDeltaTests.test_durationfield_multiply_divide',
            },
        }

        return skips

    @cached_property
    def _tidb_storage_engine(self):
        "Internal method used in Django tests. Don't rely on this from your code"
        return self.connection.tidb_server_data['default_storage_engine']

    @cached_property
    def allows_auto_pk_0(self):
        """
        Autoincrement primary key can be set to 0 if it doesn't generate new
        autoincrement values.
        """
        return 'NO_AUTO_VALUE_ON_ZERO' in self.connection.sql_mode

    @cached_property
    def can_introspect_foreign_keys(self):
        "Confirm support for introspected foreign keys"
        return False

    @cached_property
    def introspected_field_types(self):
        return {
            **super().introspected_field_types,
            'BinaryField': 'TextField',
            'BooleanField': 'IntegerField',
            'DurationField': 'BigIntegerField',
            'GenericIPAddressField': 'CharField',
        }

    @cached_property
    def has_zoneinfo_database(self):
        return self.connection.tidb_server_data['has_zoneinfo_database']

    @cached_property
    def is_sql_auto_is_null_enabled(self):
        return self.connection.tidb_server_data['sql_auto_is_null']

    @cached_property
    def supported_explain_formats(self):
        return {'ROW', 'DOT', 'JSON', 'HINT', 'VERBOSE', 'BRIEF'}

    @cached_property
    def ignores_table_name_case(self):
        return self.connection.tidb_server_data['lower_case_table_names']

    @cached_property
    def can_introspect_json_field(self):
        if self.connection.tidb_is_mariadb:
            return self.supports_json_field and self.can_introspect_check_constraints
        return self.supports_json_field
