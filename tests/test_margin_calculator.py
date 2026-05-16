import builtins
from unittest.mock import patch, MagicMock
from data_fetching_system.options_chains import margin_calculator as mc

def test_margin_calculator_mocked():
    fake_contract = {
        "symbol": "RELIANCE",
        "exchange": "NSE",
        "token": "123456",
        "lot_size": 1,
        "type": "EQ"
    }

    fake_margin_response = {
        "status": True,
        "data": {
            "totalMarginRequired": 3500,
            "marginComponents": {
                "span": 3000,
                "exposure": 500
            }
        }
    }

    with patch.object(mc, "load_contract", return_value=fake_contract):
        with patch("data_fetching_system.options_chains.margin_calculator.requests.post") as mock_post:
            mock_post.return_value = MagicMock(status_code=200)
            mock_post.return_value.json.return_value = fake_margin_response

            result = mc.calculate_margin(
                symbol="RELIANCE",
                entry=2800,
                capital=10000,
                trade_type="BUY",
                generate_report=False
            )

            assert result["margin_required"] == 3500
            assert result["capital_sufficient"] is True
            assert result["confidence_score"] > 50
            assert result["net_pnl"] < result["gross_pnl"]
            print("\n✅ MOCKED TEST PASSED: Margin calc + tax logic + scoring verified")
            for k, v in result.items():
                print(f"{k}: {v}")

if __name__ == "__main__":
    print("🧪 Running mocked margin calculator test")
    test_margin_calculator_mocked()
