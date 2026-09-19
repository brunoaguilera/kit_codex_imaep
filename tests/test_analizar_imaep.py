from __future__ import annotations

import math
import unittest
from pathlib import Path

from analizar_imaep import (
    END,
    EXPECTED_OBSERVATIONS,
    START,
    calculate_statistics,
    load_workbook_data,
    month_sequence,
    read_clean_csv,
    validate_calendar,
)


ROOT = Path(__file__).resolve().parents[1]
EXCEL = ROOT / "data/raw/imaep_bcp_original.xlsx"
CSV = ROOT / "data/processed/imaep_2016_2025.csv"


class ImaepQualityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = load_workbook_data(EXCEL)

    def test_expected_coverage(self) -> None:
        dates = [item.fecha for item in self.data.observations]
        self.assertEqual(EXPECTED_OBSERVATIONS, len(dates))
        self.assertEqual(month_sequence(START, END), dates)

    def test_no_duplicates_or_missing_months(self) -> None:
        duplicates, missing = validate_calendar(self.data.observations)
        self.assertEqual([], duplicates)
        self.assertEqual([], missing)

    def test_primary_and_secondary_series_are_equal(self) -> None:
        self.assertTrue(self.data.secondary_equal)

    def test_csv_is_exactly_equivalent_to_excel(self) -> None:
        csv_rows = read_clean_csv(CSV)
        excel_rows = [(item.fecha, item.imaep) for item in self.data.observations]
        self.assertEqual(excel_rows, csv_rows)

    def test_standard_deviation_squared_matches_variance(self) -> None:
        stats = calculate_statistics(self.data.observations)
        self.assertTrue(
            math.isclose(
                stats["desviacion_estandar_muestral"] ** 2,
                stats["varianza_muestral"],
                rel_tol=1e-12,
                abs_tol=1e-12,
            )
        )


if __name__ == "__main__":
    unittest.main()
