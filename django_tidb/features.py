import operator

from django.db.backends.base.features import BaseDatabaseFeatures
from django.utils.functional import cached_property
from django.db.backends.mysql.features import (
    DatabaseFeatures as MysqlDatabaseFeatures,
)


class DatabaseFeatures(MysqlDatabaseFeatures):
    has_select_for_update = False
    supports_transactions = False
    uses_savepoints = False
    can_release_savepoints = False
    atomic_transactions = False
    supports_atomic_references_rename = False
    can_clone_databases = False
    can_rollback_ddl = False
    order_by_nulls_first = False
    supports_foreign_keys = False
    indexes_foreign_keys = False
    test_collations = {
        'ci': 'utf8_general_ci',
        'non_default': 'utf8mb4_unicode_ci',
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
                'aggregation.tests.AggregateTestCase.test_sum_duration_field',
                'aggregation.tests.AggregateTestCase.test_avg_duration_field',
                'aggregation.tests.AggregateTestCase.test_aggregation_random_ordering',

                'lookup.tests.LookupTests.test_regex',

                'queries.tests.ComparisonTests.test_ticket8597',
                'queries.test_qs_combinators.QuerySetSetOperationTests.test_union_with_values_list_and_order_on_annotation',
                'queries.test_qs_combinators.QuerySetSetOperationTests.test_union_with_values_list_and_order',
                'queries.test_qs_combinators.QuerySetSetOperationTests.test_ordering_subqueries',
                'queries.test_qs_combinators.QuerySetSetOperationTests.test_ordering_by_f_expression_and_alias',
                'queries.test_qs_combinators.QuerySetSetOperationTests.test_ordering_by_f_expression',
                'queries.test_qs_combinators.QuerySetSetOperationTests.test_ordering_by_alias',
                'queries.test_qs_combinators.QuerySetSetOperationTests.test_ordering',
                'queries.test_qs_combinators.QuerySetSetOperationTests.test_order_by_same_type',
                'queries.test_qs_combinators.QuerySetSetOperationTests.test_combining_multiple_models',

                # is unrelation with tidb
                'file_uploads.tests.DirectoryCreationTests.test_readonly_root',
                'cache.tests.CacheMiddlewareTest.test_cache_page_timeout',

                # interface conversion: interface {} is int64, not uint64'
                # https://github.com/pingcap/tidb/issues/25956
                'expressions_window.tests.WindowFunctionTests.test_max_per_year',
                'expressions_window.tests.WindowFunctionTests.test_min_department',
                'expressions_window.tests.WindowFunctionTests.test_multiple_partitioning',

                # RuntimeError: A durable atomic block cannot be nested within another atomic block.
                'transactions.tests.DisableDurabiltityCheckTests.test_nested_both_durable',
                'transactions.tests.DisableDurabiltityCheckTests.test_nested_inner_durable',

                # wrong test result
                'transaction_hooks.tests.TestConnectionOnCommit.test_inner_savepoint_does_not_affect_outer',
                'filtered_relation.tests.FilteredRelationTests.test_as_subquery',
                'filtered_relation.tests.FilteredRelationTests.test_defer',
                'filtered_relation.tests.FilteredRelationTests.test_exclude_relation_with_join',
                'filtered_relation.tests.FilteredRelationTests.test_extra',
                'filtered_relation.tests.FilteredRelationTests.test_multiple_times',
                'filtered_relation.tests.FilteredRelationTests.test_select_for_update',
                'filtered_relation.tests.FilteredRelationTests.test_union',
                'filtered_relation.tests.FilteredRelationTests.test_values',
                'filtered_relation.tests.FilteredRelationTests.test_values_list',
                'filtered_relation.tests.FilteredRelationTests.test_with_exclude',
                'filtered_relation.tests.FilteredRelationTests.test_with_join',
                'filtered_relation.tests.FilteredRelationTests.test_with_join_and_complex_condition',
                'fixtures_regress.tests.TestFixtures.test_loaddata_raises_error_when_fixture_has_invalid_foreign_key',

                # django.db.transaction.TransactionManagementError: An error occurred in the current transaction. You
                # can't execute queries until the end of the 'atomic' block.
                'transaction_hooks.tests.TestConnectionOnCommit.test_inner_savepoint_rolled_back_with_outer',
                'transaction_hooks.tests.TestConnectionOnCommit.test_discards_hooks_from_rolled_back_savepoint',

                # AssertionError: True is not false
                'sites_tests.tests.CreateDefaultSiteTests.test_multi_db_with_router',
                # AssertionError: {} != {'example2.com': <Site: example2.com>}
                'sites_tests.tests.SitesFrameworkTests.test_clear_site_cache_domain',

                # AttributeError: 'NoneType' object has no attribute 'ping'
                'servers.test_liveserverthread.LiveServerThreadTest.test_closes_connections',

                'test_utils.tests.TestBadSetUpTestData.test_failure_in_setUpTestData_should_rollback_transaction',
                'test_utils.test_testcase.TestDataTests.test_undeepcopyable_warning',
                'test_utils.test_testcase.TestDataTests.test_class_attribute_identity',
                'test_utils.tests.CaptureOnCommitCallbacksTests.test_execute',
                'test_utils.tests.CaptureOnCommitCallbacksTests.test_no_arguments',
                'test_utils.tests.CaptureOnCommitCallbacksTests.test_pre_callback',
                'test_utils.tests.CaptureOnCommitCallbacksTests.test_using',

                # not support ORDER BY RANDOM() ASC
                'ordering.tests.OrderingTests.test_random_ordering',

                # [planner:3065]Expression #1 of ORDER BY clause is not in SELECT list, references column '' which is
                # not in SELECT list; this is incompatible with
                'ordering.tests.OrderingTests.test_orders_nulls_first_on_filtered_subquery',

                # You have an error in your SQL syntax
                'schema.tests.SchemaTests.test_add_field_binary',
                'schema.tests.SchemaTests.test_add_textfield_default_nullable',
                'schema.tests.SchemaTests.test_add_textfield_unhashable_default',

                # Unsupported modify column: this column has primary key flag
                'schema.tests.SchemaTests.test_alter_auto_field_to_char_field',

                # Unsupported modify column: can't remove auto_increment without @@tidb_allow_remove_auto_inc enabled
                'schema.tests.SchemaTests.test_alter_auto_field_to_integer_field',

                # 'Unsupported modify column: this column has primary key flag
                'schema.tests.SchemaTests.test_alter_autofield_pk_to_smallautofield_pk_sequence_owner',

                # Found wrong number (0) of check constraints for schema_author.height
                'schema.tests.SchemaTests.test_alter_field_default_dropped',

                # Unsupported modify column: can't set auto_increment
                'schema.tests.SchemaTests.test_alter_int_pk_to_autofield_pk',
                'schema.tests.SchemaTests.test_alter_int_pk_to_bigautofield_pk',

                # Unsupported drop primary key when the table's pkIsHandle is true
                'schema.tests.SchemaTests.test_alter_int_pk_to_int_unique',

                # Unsupported drop integer primary key
                'schema.tests.SchemaTests.test_alter_not_unique_field_to_primary_key',

                # Unsupported modify column: can't set auto_increment
                'schema.tests.SchemaTests.test_alter_smallint_pk_to_smallautofield_pk',

                # BLOB/TEXT/JSON column 'address' can't have a default value
                'schema.tests.SchemaTests.test_alter_text_field_to_not_null_with_default_value',

                # Unsupported modify column: this column has primary key flag
                'schema.tests.SchemaTests.test_char_field_pk_to_auto_field',

                # Unsupported modify charset from utf8mb4 to utf8
                'schema.tests.SchemaTests.test_ci_cs_db_collation',

                # Unsupported drop integer primary key
                'schema.tests.SchemaTests.test_primary_key',

                # wrong result
                'schema.tests.SchemaTests.test_alter_pk_with_self_referential_field',
                'schema.tests.SchemaTests.test_db_table',
                'schema.tests.SchemaTests.test_indexes',
                'schema.tests.SchemaTests.test_inline_fk',
                'schema.tests.SchemaTests.test_remove_constraints_capital_letters',
                'schema.tests.SchemaTests.test_remove_db_index_doesnt_remove_custom_indexes',
                'schema.tests.SchemaTests.test_rename_column_renames_deferred_sql_references',
                'schema.tests.SchemaTests.test_rename_referenced_field',
                'schema.tests.SchemaTests.test_rename_table_renames_deferred_sql_references',

                # Expression #2 of SELECT list is not in GROUP BY clause and contains nonaggregated column
                # 'test_django_tests.annotations_book.id' which is not functionally dependent on columns in GROUP BY
                # clause; this is incompatible with sql_mode=only_full_group_by
                'annotations.tests.NonAggregateAnnotationTestCase.test_annotation_aggregate_with_m2o',

                # Unknown column 'annotations_publisher.id' in 'where clause'
                'annotations.tests.NonAggregateAnnotationTestCase.test_annotation_filter_with_subquery',

                # Duplicate entry 'admin' for key 'username'
                'auth_tests.test_admin_multidb.MultiDatabaseTests.test_add_view',

                # Duplicate entry 'app_b-examplemodelb' for key 'django_content_type_app_label_model_76bd3d3b_uniq'
                'auth_tests.test_models.LoadDataWithNaturalKeysAndMultipleDatabasesTestCase'
                '.test_load_data_with_user_permissions',

                'auth_tests.test_views.ChangelistTests.test_view_user_password_is_readonly',
                'auth_tests.test_migrations.MultiDBProxyModelAppLabelTests',
                'auth_tests.test_management.GetDefaultUsernameTestCase.test_with_database',

                # You have an error in your SQL syntax; check the manual that corresponds to your TiDB
                # version for the right syntax to use line 2 column 25 near "PROCEDURE test_procedure
                # (P_I INTEGER)\n        BEGIN\n            DECLARE V_I INTEGER;\n            SET V_I
                # = P_I;\n        END;\n    "
                'backends.test_utils.CursorWrapperTests.test_callproc_with_int_params',

                # You have an error in your SQL syntax; check the manual that corresponds to your TiDB
                # version for the right syntax to use line 2 column 25 near "PROCEDURE test_procedure ()\n
                # BEGIN\n            DECLARE V_I INTEGER;\n            SET V_I = 1;\n        END;\n    "
                'backends.test_utils.CursorWrapperTests.test_callproc_without_params',

                'backends.base.test_base.ExecuteWrapperTests.test_nested_wrapper_invoked',
                'backends.base.test_base.ExecuteWrapperTests.test_outer_wrapper_blocks',
                'backends.tests.FkConstraintsTests.test_check_constraints',
                'backends.tests.FkConstraintsTests.test_check_constraints_sql_keywords',

                # ignore multi database
                'contenttypes_tests.test_models.ContentTypesMultidbTests.test_multidb',

                # ContentType matching query does not exist. 
                'contenttypes_tests.test_models.ContentTypesTests.test_app_labeled_name',

                # IntegrityError not raised
                'constraints.tests.CheckConstraintTests.test_database_constraint',
                'constraints.tests.CheckConstraintTests.test_database_constraint_expression',
                'constraints.tests.CheckConstraintTests.test_database_constraint_expressionwrapper',
                'constraints.tests.CheckConstraintTests.test_database_constraint_unicode',

                # Cannot assign "<Book: Book object (90)>": the current database router prevents this relation.
                'prefetch_related.tests.MultiDbTests.test_using_is_honored_custom_qs',
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
        return False

    @cached_property
    def supports_explain_analyze(self):
        return True

    @cached_property
    def supported_explain_formats(self):
        return {'DOT', 'ROW', 'BRIEF'}

    @cached_property
    def ignores_table_name_case(self):
        return self.connection.tidb_server_data['lower_case_table_names']

    @cached_property
    def supports_default_in_lead_lag(self):
        return True

    @cached_property
    def supports_json_field(self):
        return False

    @cached_property
    def can_introspect_json_field(self):
        return self.supports_json_field and self.can_introspect_check_constraints

    @cached_property
    def supports_index_column_ordering(self):
        return False

    @cached_property
    def supports_expression_indexes(self):
        return True
