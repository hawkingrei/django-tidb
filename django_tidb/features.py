
import operator

from django.db.backends.base.features import BaseDatabaseFeatures
from django.utils.functional import cached_property
from django.db.backends.mysql.feature import (
    DatabaseFeatures as MysqlDatabaseFeatures,
)

class DatabaseFeatures(MysqlDatabaseFeatures):

    supports_transactions = False
    uses_savepoints = False
    can_release_savepoints = False
    atomic_transactions = False
    supports_atomic_references_rename = False
    can_clone_databases = False
    can_rollback_ddl = False

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
            "tidb": {
                # https://github.com/pingcap/tidb/issues/25883
                'or_lookups.tests.OrLookupsTests.test_empty_in',

                # "Expression #5 of SELECT list is not in GROUP BY clause and contains nonaggregated column
                # 'test_django_tests.aggregation_regress_alfa.id' which is not functionally dependent on columns in
                # GROUP BY clause; this is incompatible with sql_mode=only_full_group_by"
                'aggregation.tests.AggregateTestCase.test_annotate_defer_select_related',
                'aggregation_regress.tests.AggregationTests.test_aggregate_duplicate_columns_select_related',
                'aggregation_regress.tests.AggregationTests.test_boolean_conversion',
                'aggregation_regress.tests.AggregationTests.test_more_more',
                'aggregation_regress.tests.JoinPromotionTests.test_ticket_21150',

                # Unsupported multi schema change
                'indexes.tests.SchemaIndexesMySQLTests.test_no_index_for_foreignkey',
                
                'lookup.tests.LookupTests.test_regex'
            }
        }
        return skips

    @cached_property
    def update_can_self_select(self):
        return True

    @cached_property
    def can_introspect_foreign_keys(self):
        "Confirm support for introspected foreign keys"
        return False

    @cached_property
    def can_return_columns_from_insert(self):
        return False

    can_return_rows_from_bulk_insert = property(operator.attrgetter('can_return_columns_from_insert'))

    @cached_property
    def has_zoneinfo_database(self):
        return self.connection.tidb_server_data['has_zoneinfo_database']

    @cached_property
    def is_sql_auto_is_null_enabled(self):
        return self.connection.tidb_server_data['sql_auto_is_null']

    @cached_property
    def supports_over_clause(self):
        return True

    supports_frame_range_fixed_distance = property(operator.attrgetter('supports_over_clause'))

    @cached_property
    def supports_column_check_constraints(self):
        return True

    supports_table_check_constraints = property(operator.attrgetter('supports_column_check_constraints'))

    @cached_property
    def can_introspect_check_constraints(self):
        return False

    @cached_property
    def has_select_for_update_skip_locked(self):
        return False

    @cached_property
    def has_select_for_update_nowait(self):
        return False

    @cached_property
    def has_select_for_update_of(self):
        return True

    @cached_property
    def supports_explain_analyze(self):
        return True

    @cached_property
    def supported_explain_formats(self):
        return {'ROW', 'DOT', 'JSON', 'HINT', 'VERBOSE', 'BRIEF'}

    @cached_property
    def ignores_table_name_case(self):
        return self.connection.tidb_server_data['lower_case_table_names']

    @cached_property
    def supports_default_in_lead_lag(self):
        return True

    @cached_property
    def supports_json_field(self):
        return True

    @cached_property
    def can_introspect_json_field(self):
        return self.supports_json_field and self.can_introspect_check_constraints

    @cached_property
    def supports_index_column_ordering(self):
        return False

    @cached_property
    def supports_expression_indexes(self):
        return False