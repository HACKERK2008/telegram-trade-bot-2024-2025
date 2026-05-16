# strategy/base_strategy.py

from abc import ABC, abstractmethod
import pandas as pd

class BaseStrategy(ABC):
    """
    Abstract base class for all strategies. 
    Forces standard interface and allows plug-in flexibility.
    """

    def __init__(self, name: str = "UnnamedStrategy"):
        self.name = name

    @abstractmethod
    def generate_signal(self, df: pd.DataFrame) -> str:
        """
        Returns a signal like 'up' or 'down' or 'neutral'.
        Must be implemented by all child strategies.
        """
        pass

    def describe(self) -> str:
        """
        Optional docstring or user-friendly explanation.
        """
        return f"📊 Strategy: {self.name}"
