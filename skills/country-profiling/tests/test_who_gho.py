import unittest

from pathlib import Path
import sys

SCRIPT_DIR = Path(__file__).resolve().parents[1] / "sourcing_scripts"
sys.path.insert(0, str(SCRIPT_DIR))

import who_gho


class WhoGhoParsingTests(unittest.TestCase):
    def test_latest_country_row_selects_latest_non_empty_value(self):
        payload = {
            "value": [
                {"SpatialDim": "ITA", "TimeDim": 2022, "NumericValue": 91.0, "Value": "91"},
                {"SpatialDim": "ITA", "TimeDim": 2024, "NumericValue": 95.0, "Value": "95"},
                {"SpatialDim": "ITA", "TimeDim": 2023, "NumericValue": None, "Value": None},
                {"SpatialDim": "FRA", "TimeDim": 2025, "NumericValue": 99.0, "Value": "99"},
            ]
        }

        row = who_gho.latest_country_row(payload, "ITA")

        self.assertIsNotNone(row)
        self.assertEqual(row["TimeDim"], 2024)
        self.assertEqual(row["NumericValue"], 95.0)

    def test_latest_country_row_returns_none_for_missing_country(self):
        payload = {"value": [{"SpatialDim": "FRA", "TimeDim": 2024, "NumericValue": 95.0}]}

        row = who_gho.latest_country_row(payload, "ITA")

        self.assertIsNone(row)

    def test_immunization_focus_returns_configured_indicators(self):
        indicators = who_gho.configured_indicators_for_focus("immunization")

        self.assertEqual(
            [indicator["indicator_code"] for indicator in indicators],
            ["WHS4_100", "WHS8_110", "MCV2", "PCV3"],
        )


if __name__ == "__main__":
    unittest.main()
