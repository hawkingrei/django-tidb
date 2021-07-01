
import operator

from django.db.backends.base.features import BaseDatabaseFeatures
from django.utils.functional import cached_property


class DatabaseFeatures(BaseDatabaseFeatures):
    empty_fetchmany_value = ()
    allows_group_by_pk = True
    uses_savepoints = False
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
    # Django tests that aren't supported by Spanner.
    skip_tests = (
        # No foreign key constraints in Spanner.
        "backends.tests.FkConstraintsTests.test_check_constraints",
        "fixtures_regress.tests.TestFixtures.test_loaddata_raises_error_when_fixture_has_invalid_foreign_key",
        # No Django transaction management in Spanner.
        "basic.tests.SelectOnSaveTests.test_select_on_save_lying_update",
        # django_spanner monkey patches AutoField to have a default value.
        "basic.tests.ModelTest.test_hash",
        "custom_managers.tests.CustomManagerTests.test_slow_removal_through_specified_fk_related_manager",
        "custom_managers.tests.CustomManagerTests.test_slow_removal_through_default_fk_related_manager",
        "generic_relations.test_forms.GenericInlineFormsetTests.test_options",
        "generic_relations.tests.GenericRelationsTests.test_add_bulk_false",
        "generic_relations.tests.GenericRelationsTests.test_generic_update_or_create_when_updated",
        "generic_relations.tests.GenericRelationsTests.test_update_or_create_defaults",
        "generic_relations.tests.GenericRelationsTests.test_unsaved_instance_on_generic_foreign_key",
        "generic_relations_regress.tests.GenericRelationTests.test_target_model_is_unsaved",
        "m2m_through_regress.tests.ToFieldThroughTests.test_m2m_relations_unusable_on_null_pk_obj",
        "many_to_many.tests.ManyToManyTests.test_add",
        "many_to_one.tests.ManyToOneTests.test_fk_assignment_and_related_object_cache",
        "many_to_one.tests.ManyToOneTests.test_relation_unsaved",
        "model_fields.test_durationfield.TestSerialization.test_dumping",
        "model_fields.test_uuid.TestSerialization.test_dumping",
        "model_fields.test_booleanfield.ValidationTest.test_nullbooleanfield_blank",
        "model_inheritance.tests.ModelInheritanceTests.test_create_child_no_update",
        "model_regress.tests.ModelTests.test_get_next_prev_by_field_unsaved",
        "one_to_one.tests.OneToOneTests.test_get_reverse_on_unsaved_object",
        "one_to_one.tests.OneToOneTests.test_o2o_primary_key_delete",
        "one_to_one.tests.OneToOneTests.test_set_reverse_on_unsaved_object",
        "one_to_one.tests.OneToOneTests.test_unsaved_object",
        "queries.test_bulk_update.BulkUpdateNoteTests.test_unsaved_models",
        "expressions_case.tests.CaseExpressionTests.test_update_decimal",
        "serializers.test_json.JsonSerializerTestCase.test_pkless_serialized_strings",
        "serializers.test_json.JsonSerializerTestCase.test_serialize_with_null_pk",
        "serializers.test_xml.XmlSerializerTestCase.test_pkless_serialized_strings",
        "serializers.test_xml.XmlSerializerTestCase.test_serialize_with_null_pk",
        "serializers.test_yaml.YamlSerializerTestCase.test_pkless_serialized_strings",
        "serializers.test_yaml.YamlSerializerTestCase.test_serialize_with_null_pk",
        "serializers.test_data.SerializerDataTests.test_yaml_serializer",
        "serializers.test_data.SerializerDataTests.test_xml_serializer",
        "serializers.test_data.SerializerDataTests.test_python_serializer",
        "serializers.test_data.SerializerDataTests.test_json_serializer",
        "timezones.tests.LegacyDatabaseTests.test_cursor_execute_accepts_naive_datetime",
        "timezones.tests.NewDatabaseTests.test_cursor_execute_accepts_naive_datetime",
        "timezones.tests.AdminTests.test_change_editable",
        "timezones.tests.AdminTests.test_change_editable_in_other_timezone",
        "timezones.tests.AdminTests.test_change_readonly",
        "timezones.tests.AdminTests.test_change_readonly_in_other_timezone",
        "timezones.tests.AdminTests.test_changelist",
        "timezones.tests.AdminTests.test_changelist_in_other_timezone",
        "validation.test_custom_messages.CustomMessagesTests.test_custom_null_message",
        "validation.test_custom_messages.CustomMessagesTests.test_custom_simple_validator_message",
        "validation.test_unique.PerformUniqueChecksTest.test_primary_key_unique_check_not_performed_when_adding_and_pk_not_specified",
        # noqa
        "validation.test_unique.PerformUniqueChecksTest.test_primary_key_unique_check_not_performed_when_not_adding",
        "validation.test_validators.TestModelsWithValidators.test_custom_validator_passes_for_correct_value",
        "validation.test_validators.TestModelsWithValidators.test_custom_validator_raises_error_for_incorrect_value",
        "validation.test_validators.TestModelsWithValidators.test_field_validators_can_be_any_iterable",
        # Tests that assume a serial pk.
        "admin_filters.tests.ListFiltersTests.test_booleanfieldlistfilter_nullbooleanfield",
        "admin_filters.tests.ListFiltersTests.test_booleanfieldlistfilter_tuple",
        "admin_filters.tests.ListFiltersTests.test_booleanfieldlistfilter",
        "admin_filters.tests.ListFiltersTests.test_datefieldlistfilter_with_time_zone_support",
        "admin_filters.tests.ListFiltersTests.test_datefieldlistfilter",
        "admin_filters.tests.ListFiltersTests.test_fieldlistfilter_underscorelookup_tuple",
        "admin_filters.tests.ListFiltersTests.test_fk_with_to_field",
        "admin_filters.tests.ListFiltersTests.test_listfilter_genericrelation",
        "admin_filters.tests.ListFiltersTests.test_lookup_with_non_string_value_underscored",
        "admin_filters.tests.ListFiltersTests.test_lookup_with_non_string_value",
        "admin_filters.tests.ListFiltersTests.test_relatedfieldlistfilter_manytomany",
        "admin_filters.tests.ListFiltersTests.test_simplelistfilter",
        "admin_inlines.tests.TestInline.test_inline_hidden_field_no_column",
        "proxy_models.tests.ProxyModelAdminTests.test_delete_str_in_model_admin",
        "admin_utils.test_logentry.LogEntryTests.test_logentry_change_message",
        "admin_utils.test_logentry.LogEntryTests.test_logentry_change_message_localized_datetime_input",
        "admin_utils.test_logentry.LogEntryTests.test_proxy_model_content_type_is_used_for_log_entries",
        "admin_utils.test_logentry.LogEntryTests.test_action_flag_choices",
        "admin_utils.test_logentry.LogEntryTests.test_log_action",
        "admin_utils.test_logentry.LogEntryTests.test_logentry_change_message_formsets",
        "admin_utils.test_logentry.LogEntryTests.test_logentry_change_message_not_json",
        "admin_utils.test_logentry.LogEntryTests.test_logentry_get_admin_url",
        "admin_utils.test_logentry.LogEntryTests.test_logentry_get_edited_object",
        "admin_utils.test_logentry.LogEntryTests.test_logentry_repr",
        "admin_utils.test_logentry.LogEntryTests.test_logentry_save",
        "admin_utils.test_logentry.LogEntryTests.test_logentry_unicode",
        "admin_utils.test_logentry.LogEntryTests.test_recentactions_without_content_type",
        "admin_views.tests.AdminViewPermissionsTest.test_history_view",
        "aggregation.test_filter_argument.FilteredAggregateTests.test_plain_annotate",
        "aggregation.tests.AggregateTestCase.test_annotate_basic",
        "aggregation.tests.AggregateTestCase.test_annotation",
        "aggregation.tests.AggregateTestCase.test_filtering",
        "aggregation_regress.tests.AggregationTests.test_more_more",
        "aggregation_regress.tests.AggregationTests.test_more_more_more",
        "aggregation_regress.tests.AggregationTests.test_ticket_11293",
        "defer_regress.tests.DeferRegressionTest.test_ticket_12163",
        "defer_regress.tests.DeferRegressionTest.test_ticket_23270",
        "distinct_on_fields.tests.DistinctOnTests.test_basic_distinct_on",
        "extra_regress.tests.ExtraRegressTests.test_regression_7314_7372",
        "generic_relations_regress.tests.GenericRelationTests.test_annotate",
        "get_earliest_or_latest.tests.TestFirstLast",
        "known_related_objects.tests.ExistingRelatedInstancesTests.test_reverse_one_to_one_multi_prefetch_related",
        "known_related_objects.tests.ExistingRelatedInstancesTests.test_reverse_one_to_one_multi_select_related",
        "lookup.tests.LookupTests.test_get_next_previous_by",
        "lookup.tests.LookupTests.test_values_list",
        "migrations.test_operations.OperationTests.test_alter_order_with_respect_to",
        "model_fields.tests.GetChoicesOrderingTests.test_get_choices_reverse_related_field",
        "model_formsets.tests.ModelFormsetTest.test_custom_pk",
        "model_formsets_regress.tests.FormfieldShouldDeleteFormTests.test_custom_delete",
        "multiple_database.tests.RouterTestCase.test_generic_key_cross_database_protection",
        "ordering.tests.OrderingTests.test_default_ordering_by_f_expression",
        "ordering.tests.OrderingTests.test_order_by_fk_attname",
        "ordering.tests.OrderingTests.test_order_by_override",
        "ordering.tests.OrderingTests.test_order_by_pk",
        "prefetch_related.test_prefetch_related_objects.PrefetchRelatedObjectsTests.test_m2m_then_m2m",
        "prefetch_related.tests.CustomPrefetchTests.test_custom_qs",
        "prefetch_related.tests.CustomPrefetchTests.test_nested_prefetch_related_are_not_overwritten",
        "prefetch_related.tests.DirectPrefechedObjectCacheReuseTests.test_detect_is_fetched",
        "prefetch_related.tests.DirectPrefechedObjectCacheReuseTests.test_detect_is_fetched_with_to_attr",
        "prefetch_related.tests.ForeignKeyToFieldTest.test_m2m",
        "queries.test_bulk_update.BulkUpdateNoteTests.test_multiple_fields",
        "queries.test_bulk_update.BulkUpdateTests.test_inherited_fields",
        "queries.tests.Queries1Tests.test_ticket9411",
        "queries.tests.Queries4Tests.test_ticket15316_exclude_true",
        "queries.tests.Queries5Tests.test_ticket7256",
        "queries.tests.SubqueryTests.test_related_sliced_subquery",
        "queries.tests.Ticket14056Tests.test_ticket_14056",
        "queries.tests.RelatedLookupTypeTests.test_values_queryset_lookup",
        "raw_query.tests.RawQueryTests.test_annotations",
        "raw_query.tests.RawQueryTests.test_get_item",
        "select_related.tests.SelectRelatedTests.test_field_traversal",
        "syndication_tests.tests.SyndicationFeedTest.test_rss2_feed",
        "syndication_tests.tests.SyndicationFeedTest.test_latest_post_date",
        "syndication_tests.tests.SyndicationFeedTest.test_rss091_feed",
        "syndication_tests.tests.SyndicationFeedTest.test_template_feed",
        # datetimes retrieved from the database with the wrong hour when
        # USE_TZ = True: https://github.com/googleapis/python-spanner-django/issues/193
        "datetimes.tests.DateTimesTests.test_21432",
        "db_functions.datetime.test_extract_trunc.DateFunctionWithTimeZoneTests.test_trunc_func_with_timezone",
        "db_functions.datetime.test_extract_trunc.DateFunctionWithTimeZoneTests.test_trunc_timezone_applied_before_truncation",
        # noqa
        # extract() with timezone not working as expected:
        # https://github.com/googleapis/python-spanner-django/issues/191
        "timezones.tests.NewDatabaseTests.test_query_datetimes",
        # using NULL with + crashes: https://github.com/googleapis/python-spanner-django/issues/201
        "annotations.tests.NonAggregateAnnotationTestCase.test_combined_annotation_commutative",
        # Spanner loses DecimalField precision due to conversion to float:
        # https://github.com/googleapis/python-spanner-django/pull/133#pullrequestreview-328482925
        "aggregation.tests.AggregateTestCase.test_decimal_max_digits_has_no_effect",
        "aggregation.tests.AggregateTestCase.test_related_aggregate",
        "db_functions.comparison.test_cast.CastTests.test_cast_to_decimal_field",
        "model_fields.test_decimalfield.DecimalFieldTests.test_fetch_from_db_without_float_rounding",
        "model_fields.test_decimalfield.DecimalFieldTests.test_roundtrip_with_trailing_zeros",
        # No CHECK constraints in Spanner.
        "model_fields.test_integerfield.PositiveIntegerFieldTests.test_negative_values",
        # Spanner doesn't support the variance the standard deviation database
        # functions:
        "aggregation.test_filter_argument.FilteredAggregateTests.test_filtered_numerical_aggregates",
        "aggregation_regress.tests.AggregationTests.test_stddev",
        # SELECT list expression references <column> which is neither grouped
        # nor aggregated: https://github.com/googleapis/python-spanner-django/issues/245
        "aggregation_regress.tests.AggregationTests.test_annotated_conditional_aggregate",
        "aggregation_regress.tests.AggregationTests.test_annotation_with_value",
        "expressions.tests.BasicExpressionsTests.test_filtering_on_annotate_that_uses_q",
        # "No matching signature for operator" crash when comparing TIMESTAMP
        # and DATE: https://github.com/googleapis/python-spanner-django/issues/255
        "expressions.tests.BasicExpressionsTests.test_outerref_mixed_case_table_name",
        "expressions.tests.FTimeDeltaTests.test_mixed_comparisons1",
        # duration arithmetic fails with dates: No matching signature for
        # function TIMESTAMP_ADD: https://github.com/googleapis/python-spanner-django/issues/253
        "expressions.tests.FTimeDeltaTests.test_date_comparison",
        "expressions.tests.FTimeDeltaTests.test_date_minus_duration",
        "expressions.tests.FTimeDeltaTests.test_delta_add",
        "expressions.tests.FTimeDeltaTests.test_duration_with_datetime",
        "expressions.tests.FTimeDeltaTests.test_mixed_comparisons2",
        # This test doesn't raise NotSupportedError because Spanner doesn't
        # support select for update either (besides the "with limit"
        # restriction).
        "select_for_update.tests.SelectForUpdateTests.test_unsupported_select_for_update_with_limit",
        # integer division produces a float result, which can't be assigned to
        # an integer column:
        # https://github.com/googleapis/python-spanner-django/issues/331
        "expressions.tests.ExpressionOperatorTests.test_lefthand_division",
        "expressions.tests.ExpressionOperatorTests.test_right_hand_division",
        # power operator produces a float result, which can't be assigned to
        # an integer column:
        # https://github.com/googleapis/python-spanner-django/issues/331
        "expressions.tests.ExpressionOperatorTests.test_lefthand_power",
        "expressions.tests.ExpressionOperatorTests.test_righthand_power",
        # Cloud Spanner's docs: "The rows that are returned by LIMIT and OFFSET
        # is unspecified unless these operators are used after ORDER BY."
        "aggregation_regress.tests.AggregationTests.test_sliced_conditional_aggregate",
        "queries.tests.QuerySetBitwiseOperationTests.test_or_with_both_slice",
        "queries.tests.QuerySetBitwiseOperationTests.test_or_with_both_slice_and_ordering",
        "queries.tests.QuerySetBitwiseOperationTests.test_or_with_lhs_slice",
        "queries.tests.QuerySetBitwiseOperationTests.test_or_with_rhs_slice",
        "queries.tests.SubqueryTests.test_slice_subquery_and_query",
        # Cloud Spanner limit: "Number of functions exceeds the maximum
        # allowed limit of 1000."
        "queries.test_bulk_update.BulkUpdateTests.test_large_batch",
        # Spanner doesn't support random ordering.
        "ordering.tests.OrderingTests.test_random_ordering",
        # casting DateField to DateTimeField adds an unexpected hour:
        # https://github.com/googleapis/python-spanner-django/issues/260
        "db_functions.comparison.test_cast.CastTests.test_cast_from_db_date_to_datetime",
        # Tests that fail during tear down on databases that don't support
        # transactions: https://github.com/googleapis/python-spanner-django/issues/271
        "admin_views.test_multidb.MultiDatabaseTests.test_add_view",
        "admin_views.test_multidb.MultiDatabaseTests.test_change_view",
        "admin_views.test_multidb.MultiDatabaseTests.test_delete_view",
        "auth_tests.test_admin_multidb.MultiDatabaseTests.test_add_view",
        "auth_tests.test_remote_user_deprecation.RemoteUserCustomTest.test_configure_user_deprecation_warning",
        "contenttypes_tests.test_models.ContentTypesMultidbTests.test_multidb",
        # Tests that by-pass using django_spanner and generate
        # invalid DDL: https://github.com/googleapis/python-spanner-django/issues/298
        "cache.tests.CreateCacheTableForDBCacheTests",
        "cache.tests.DBCacheTests",
        "cache.tests.DBCacheWithTimeZoneTests",
        "delete.tests.DeletionTests.test_queryset_delete_returns_num_rows",
        "delete.tests.DeletionTests.test_model_delete_returns_num_rows",
        "delete.tests.DeletionTests.test_deletion_order",
        "delete.tests.FastDeleteTests.test_fast_delete_empty_no_update_can_self_select",
        # Tests that require transactions.
        "transaction_hooks.tests.TestConnectionOnCommit.test_does_not_execute_if_transaction_rolled_back",
        "transaction_hooks.tests.TestConnectionOnCommit.test_hooks_cleared_after_rollback",
        "transaction_hooks.tests.TestConnectionOnCommit.test_hooks_cleared_on_reconnect",
        "transaction_hooks.tests.TestConnectionOnCommit.test_no_hooks_run_from_failed_transaction",
        "transaction_hooks.tests.TestConnectionOnCommit.test_no_savepoints_atomic_merged_with_outer",
        # Tests that require savepoints.
        "get_or_create.tests.UpdateOrCreateTests.test_integrity",
        "get_or_create.tests.UpdateOrCreateTests.test_manual_primary_key_test",
        "get_or_create.tests.UpdateOrCreateTestsWithManualPKs.test_create_with_duplicate_primary_key",
        "test_utils.tests.TestBadSetUpTestData.test_failure_in_setUpTestData_should_rollback_transaction",
        "transaction_hooks.tests.TestConnectionOnCommit.test_discards_hooks_from_rolled_back_savepoint",
        "transaction_hooks.tests.TestConnectionOnCommit.test_inner_savepoint_rolled_back_with_outer",
        "transaction_hooks.tests.TestConnectionOnCommit.test_inner_savepoint_does_not_affect_outer",
        # Spanner doesn't support views.
        "inspectdb.tests.InspectDBTransactionalTests.test_include_views",
        "introspection.tests.IntrospectionTests.test_table_names_with_views",
        # No sequence for AutoField in Spanner.
        "introspection.tests.IntrospectionTests.test_sequence_list",
        # DatabaseIntrospection.get_key_columns() is only required if this
        # backend needs it (which it currently doesn't).
        "introspection.tests.IntrospectionTests.test_get_key_columns",
        # DatabaseIntrospection.get_relations() isn't implemented:
        # https://github.com/googleapis/python-spanner-django/issues/311
        "introspection.tests.IntrospectionTests.test_get_relations",
        # pyformat parameters not supported on INSERT:
        # https://github.com/googleapis/python-spanner-django/issues/343
        "backends.tests.BackendTestCase.test_cursor_execute_with_pyformat",
        "backends.tests.BackendTestCase.test_cursor_executemany_with_pyformat",
        "backends.tests.BackendTestCase.test_cursor_executemany_with_pyformat_iterator",
        "migrations.test_commands.MigrateTests.test_migrate_fake_initial",
        "migrations.test_commands.MigrateTests.test_migrate_initial_false",
        "migrations.test_executor.ExecutorTests.test_soft_apply",
        # Spanner limitation: Cannot change type of column.
        "migrations.test_executor.ExecutorTests.test_alter_id_type_with_fk",
        "schema.tests.SchemaTests.test_alter_auto_field_to_char_field",
        "schema.tests.SchemaTests.test_alter_text_field_to_date_field",
        "schema.tests.SchemaTests.test_alter_text_field_to_datetime_field",
        "schema.tests.SchemaTests.test_alter_text_field_to_time_field",
        # Spanner limitation: Cannot rename tables and columns.
        "contenttypes_tests.test_operations.ContentTypeOperationsTests",
        "migrations.test_operations.OperationTests.test_alter_fk_non_fk",
        "migrations.test_operations.OperationTests.test_alter_model_table",
        "migrations.test_operations.OperationTests.test_alter_model_table_m2m",
        "migrations.test_operations.OperationTests.test_rename_field",
        "migrations.test_operations.OperationTests.test_rename_field_reloads_state_on_fk_target_changes",
        "migrations.test_operations.OperationTests.test_rename_m2m_model_after_rename_field",
        "migrations.test_operations.OperationTests.test_rename_m2m_target_model",
        "migrations.test_operations.OperationTests.test_rename_m2m_through_model",
        "migrations.test_operations.OperationTests.test_rename_model",
        "migrations.test_operations.OperationTests.test_rename_model_with_m2m",
        "migrations.test_operations.OperationTests.test_rename_model_with_self_referential_fk",
        "migrations.test_operations.OperationTests.test_rename_model_with_self_referential_m2m",
        "migrations.test_operations.OperationTests.test_rename_model_with_superclass_fk",
        "migrations.test_operations.OperationTests.test_repoint_field_m2m",
        "schema.tests.SchemaTests.test_alter_db_table_case",
        "schema.tests.SchemaTests.test_alter_pk_with_self_referential_field",
        "schema.tests.SchemaTests.test_rename",
        "schema.tests.SchemaTests.test_db_table",
        "schema.tests.SchemaTests.test_m2m_rename_field_in_target_model",
        "schema.tests.SchemaTests.test_m2m_repoint",
        "schema.tests.SchemaTests.test_m2m_repoint_custom",
        "schema.tests.SchemaTests.test_m2m_repoint_inherited",
        "schema.tests.SchemaTests.test_rename_column_renames_deferred_sql_references",
        "schema.tests.SchemaTests.test_rename_keep_null_status",
        "schema.tests.SchemaTests.test_rename_referenced_field",
        "schema.tests.SchemaTests.test_rename_table_renames_deferred_sql_references",
        "schema.tests.SchemaTests.test_referenced_field_without_constraint_rename_inside_atomic_block",
        "schema.tests.SchemaTests.test_referenced_table_without_constraint_rename_inside_atomic_block",
        "schema.tests.SchemaTests.test_unique_name_quoting",
        # Spanner limitation: Cannot change a field to a primary key.
        "schema.tests.SchemaTests.test_alter_not_unique_field_to_primary_key",
        # Spanner limitation: Cannot drop column in primary key.
        "schema.tests.SchemaTests.test_primary_key",
        # Spanner limitation:  Cannot remove a column from the primary key.
        "schema.tests.SchemaTests.test_alter_int_pk_to_int_unique",
        # Spanner limitation: migrations aren't atomic since Spanner doesn't
        # support transactions.
        "migrations.test_executor.ExecutorTests.test_atomic_operation_in_non_atomic_migration",
        # changing a not null constraint isn't allowed if it affects an index:
        # https://github.com/googleapis/python-spanner-django/issues/378
        "migrations.test_operations.OperationTests.test_alter_field_with_index",
        # parsing INSERT with one inlined value and one placeholder fails:
        # https://github.com/googleapis/python-spanner-django/issues/393
        "migrations.test_operations.OperationTests.test_run_sql_params",
        # This test doesn't flush the database properly:
        # https://code.djangoproject.com/ticket/31398
        "multiple_database.tests.AuthTestCase",
        # This test isn't isolated on databases like Spanner that don't
        # support transactions: https://code.djangoproject.com/ticket/31413
        "migrations.test_loader.LoaderTests.test_loading_squashed",
        # Probably due to django-spanner setting a default on AutoField:
        # https://github.com/googleapis/python-spanner-django/issues/422
        "model_inheritance_regress.tests.ModelInheritanceTest.test_issue_6755",
        # Probably due to django-spanner setting a default on AutoField:
        # https://github.com/googleapis/python-spanner-django/issues/424
        "model_forms.tests.ModelFormBasicTests.test_runtime_choicefield_populated",
        "model_forms.tests.ModelFormBasicTests.test_multi_fields",
        "model_forms.tests.ModelFormBasicTests.test_m2m_initial_callable",
        "model_forms.tests.ModelFormBasicTests.test_initial_values",
        "model_forms.tests.OtherModelFormTests.test_prefetch_related_queryset",
        "model_formsets.tests.ModelFormsetTest.test_prevent_change_outer_model_and_create_invalid_data",
        "model_formsets_regress.tests.FormfieldShouldDeleteFormTests.test_no_delete",
        "model_formsets_regress.tests.FormsetTests.test_extraneous_query_is_not_run",
        # Numeric field is not supported in primary key/unique key.
        "model_formsets.tests.ModelFormsetTest.test_inline_formsets_with_custom_pk",
        "model_forms.tests.ModelFormBaseTest.test_exclude_and_validation",
        "model_forms.tests.UniqueTest.test_unique_together",
        "model_forms.tests.UniqueTest.test_override_unique_together_message",
        # os.chmod() doesn't work on Kokoro?
        "file_uploads.tests.DirectoryCreationTests.test_readonly_root",
        # Tests that sometimes fail on Kokoro for unknown reasons.
        "contenttypes_tests.test_models.ContentTypesTests.test_cache_not_shared_between_managers",
        "migration_test_data_persistence.tests.MigrationDataNormalPersistenceTestCase.test_persistence",
        "servers.test_liveserverthread.LiveServerThreadTest.test_closes_connections",
        "servers.tests.LiveServerDatabase.test_fixtures_loaded",
        "view_tests.tests.test_csrf.CsrfViewTests.test_no_cookies",
        "view_tests.tests.test_csrf.CsrfViewTests.test_no_referer",
        "view_tests.tests.test_i18n.SetLanguageTests.test_lang_from_translated_i18n_pattern",
    )

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
