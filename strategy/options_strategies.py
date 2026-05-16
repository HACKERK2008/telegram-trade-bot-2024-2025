# strategy/options_strategies.py

from strategy.strategy_utils import find_nearest_strike

class OptionsStrategyRecommender:
    """
    Recommends an options strategy (spread/straddle/strangle) based on trend and price.
    """

    def __init__(self, step: int = 50):
        self.strike_step = step

    def recommend(self, symbol: str, trend: str, price: float, volatility: float = None) -> dict:
        """
        Suggests an option strategy.

        Args:
            symbol (str): e.g., 'RELIANCE'
            trend (str): 'up', 'down', or 'neutral'
            price (float): Current spot price
            volatility (float): Optional implied/historical vol %

        Returns:
            dict: Strategy info with name, strikes, type, and comment
        """
        atm = find_nearest_strike(price, self.strike_step)
        strategy = {}

        if trend == "up":
            strategy = {
                "name": "Bull Call Spread",
                "type": "debit",
                "legs": [
                    {"action": "BUY", "option": "CALL", "strike": atm},
                    {"action": "SELL", "option": "CALL", "strike": atm + self.strike_step}
                ],
                "comment": "Expecting moderate bullish movement"
            }

        elif trend == "down":
            strategy = {
                "name": "Bear Put Spread",
                "type": "debit",
                "legs": [
                    {"action": "BUY", "option": "PUT", "strike": atm},
                    {"action": "SELL", "option": "PUT", "strike": atm - self.strike_step}
                ],
                "comment": "Expecting limited downside"
            }

        elif trend == "neutral":
            strategy = {
                "name": "Long Straddle",
                "type": "debit",
                "legs": [
                    {"action": "BUY", "option": "CALL", "strike": atm},
                    {"action": "BUY", "option": "PUT", "strike": atm}
                ],
                "comment": "Expecting large movement, unsure direction"
            }

            # Optional: use strangle in high vol
            if volatility and volatility > 0.35:
                strategy = {
                    "name": "Long Strangle",
                    "type": "debit",
                    "legs": [
                        {"action": "BUY", "option": "CALL", "strike": atm + self.strike_step},
                        {"action": "BUY", "option": "PUT", "strike": atm - self.strike_step}
                    ],
                    "comment": "High volatility → Strangle chosen instead of straddle"
                }

        return {
            "symbol": symbol.upper(),
            "atm_strike": atm,
            "strategy": strategy
        }
