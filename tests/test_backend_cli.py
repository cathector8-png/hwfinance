import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "hwfinance"
JULIA_BACKEND = ROOT / "backends" / "julia" / "valuation.jl"


class BackendCliTests(unittest.TestCase):
    def test_backend_flag_is_accepted(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--backend", "julia", "--help"],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("hwfinance", result.stdout.lower())

    def test_julia_backend_emits_metrics_json(self):
        result = subprocess.run(
            ["julia", str(JULIA_BACKEND), "--symbol=AAPL", "--market_cap=1000", "--total_debt=200", "--cash=50", "--fcf=120", "--ebitda=300", "--beta=1.2", "--revenue_growth=0.08", "--shares_outstanding=10"],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["symbol"], "AAPL")
        self.assertIn("dcf_enterprise_value", payload)
        self.assertIn("intrinsic_value_per_share", payload)
        self.assertIn("wacc", payload)
        self.assertIn("terminal_value", payload)
        self.assertIn("sensitivity", payload)


if __name__ == "__main__":
    unittest.main()
