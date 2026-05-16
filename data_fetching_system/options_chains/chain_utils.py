# analyzer/chain_utils.py

def parse_option_chain(data: dict) -> dict:
    # Dummy version (replace with real logic)
    return {
        'atm': 23500,
        'data': data.get('records', {}).get('data', [])
    }
