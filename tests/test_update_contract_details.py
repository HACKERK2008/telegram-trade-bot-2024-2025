import os
import sys
from dotenv import load_dotenv

# Make sure root paths work
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# 🔐 Load .env
load_dotenv()

from data_fetching_system.options_chains.update_contract_details import fetch_and_save_contracts

def test_contracts():
    try:
        contracts = fetch_and_save_contracts()
        print(f"✅ Total contracts fetched and saved: {len(contracts)}")
        print("🔍 Sample contracts:")
        for i, (k, v) in enumerate(contracts.items()):
            print(f"  {k}: {v}")
            if i >= 4:
                break
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    test_contracts()
