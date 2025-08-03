"""Scatter pays game calculations"""
from src.calculations.statistics import get_random_outcome
from src.executables.executables import Executables


class GameCalculations(Executables):
    """Game specific calculations for Scatter sample game."""

    def get_display_birds(self):
        for i in range(self.config.num_display_birds):
            