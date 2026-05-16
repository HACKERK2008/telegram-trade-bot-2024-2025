import unittest
import pandas as pd
import numpy as np
from utils.data_cleaner import (
    remove_nulls,
    normalize_column,
    convert_to_datetime,
    filter_outliers
)


class TestDataCleaner(unittest.TestCase):

    def setUp(self):
        # Sample data for testing
        self.df_with_nulls = pd.DataFrame({
            'A': [1, 2, None, 4],
            'B': ['x', 'y', 'z', None]
        })

        self.df_numeric = pd.DataFrame({
            'values': [10, 20, 30, 40, 50]
        })

        self.df_datetime = pd.DataFrame({
            'dates': ['2023-01-01', '2023-02-01', 'invalid_date']
        })

        self.df_outliers = pd.DataFrame({
            'scores': [10, 12, 14, 16, 1000]
        })

    def test_remove_nulls_drop(self):
        cleaned = remove_nulls(self.df_with_nulls)
        self.assertEqual(len(cleaned), 2)

    def test_remove_nulls_fill(self):
        filled = remove_nulls(self.df_with_nulls, fill_value=0)
        self.assertFalse(filled.isnull().values.any())

    def test_normalize_column(self):
        norm_df = normalize_column(self.df_numeric.copy(), 'values')
        self.assertAlmostEqual(norm_df['values'].min(), 0.0)
        self.assertAlmostEqual(norm_df['values'].max(), 1.0)

    def test_convert_to_datetime(self):
        converted = convert_to_datetime(self.df_datetime.copy(), 'dates')
        self.assertTrue(pd.isnull(converted['dates']).sum() == 1)  # One invalid date

    def test_filter_outliers(self):
        filtered = filter_outliers(self.df_outliers.copy(), 'scores')
        self.assertNotIn(1000, filtered['scores'].values)
        self.assertEqual(len(filtered), 4)  # Should remove the outlier only


if __name__ == '__main__':
    unittest.main()
