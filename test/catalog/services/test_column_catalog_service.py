# coding=utf-8
# Copyright 2018-2022 EVA
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import unittest

from mock import MagicMock, patch

from eva.catalog.services.column_catalog_service import ColumnCatalogService


class ColumnCatalogServiceTest(unittest.TestCase):
    def test_create_should_create_all_columns(self):
        mocks = [MagicMock() for i in range(5)]
        service = ColumnCatalogService()
        service.insert_entries(mocks)
        for mock in mocks:
            mock.save.assert_called_once()

    @patch("eva.catalog.services.column_catalog_service.ColumnCatalog")
    def test_column_by_table_id_and_name_should_query_correctly(self, mocked):
        mocked.query.filter.return_value.one_or_none.return_value = "col_obj"

        service = ColumnCatalogService()
        table_id = 123
        column_name = "a"
        actual = service.filter_entry_by_table_id_and_name(table_id, column_name)
        mocked.query.filter.assert_called_with(
            mocked._table_id == table_id, mocked._name == column_name
        )
        self.assertEqual(actual, "col_obj")

    @patch("eva.catalog.services.column_catalog_service.ColumnCatalog")
    def test_column_by_table_id(self, mocked):
        mocked.query.filter.return_value.all.return_value = ["col_obj1", "col_obj2"]

        service = ColumnCatalogService()
        table_id = 123
        actual = service.filter_entries_by_table_id(table_id)
        mocked.query.filter.assert_called_with(mocked._table_id == table_id)
        self.assertEqual(actual, ["col_obj1", "col_obj2"])