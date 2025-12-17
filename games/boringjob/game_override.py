"""Overrides for boringjob gamestate."""

import random

try:
    from game_executables import GameExecutables
except ModuleNotFoundError:  # pragma: no cover - support package import
    from games.boringjob.game_executables import GameExecutables
from src.calculations.statistics import get_random_outcome


class GameStateOverride(GameExecutables):
    """Override shared gamestate behaviors."""

    def reset_book(self):
        super().reset_book()
        self.bonus_type = None

    def assign_special_sym_function(self):
        """Assign multiplier attributes to special symbols."""
        self.special_symbol_functions = {"B": [self.assign_mult_property]}

    def assign_mult_property(self, symbol):
        """Assign multiplier value to symbol."""
        mult_values = self.get_current_distribution_conditions().get("mult_values", {})
        if mult_values and self.gametype in mult_values:
            mult_value = get_random_outcome(mult_values[self.gametype])
        else:
            mult_value = self.config.mode_minimum_multiplier.get(self.betmode, 0) or 0
        symbol.assign_attribute({"multiplier": mult_value})

    def get_highest_multiplier(self) -> float:
        """Return the highest multiplier value on the active board."""
        highest = 0.0
        for reel, _ in enumerate(self.board):
            for row, _ in enumerate(self.board[reel]):
                if self.board[reel][row].check_attribute("multiplier"):
                    highest = max(highest, float(self.board[reel][row].get_attribute("multiplier")))
        return highest

    def enforce_multiplier_guarantee(self):
        """Ensure modes that require minimum multipliers meet the constraint."""
        required = self.config.mode_minimum_multiplier.get(self.betmode)
        if required is None:
            return
        current_high = self.get_highest_multiplier()
        if current_high >= required:
            return
        self.inject_multiplier(required)
        self.get_special_symbols_on_board()

    def inject_multiplier(self, target_value: float):
        """Replace a random symbol with a multiplier carrying at least the target value."""
        reel_index = random.randrange(0, self.config.num_reels)
        row_index = random.randrange(0, self.config.num_rows[reel_index])
        mult_symbol = self.create_symbol("B")
        mult_symbol.assign_attribute({"multiplier": target_value})
        self.board[reel_index][row_index] = mult_symbol

    def check_repeat(self):
        super().check_repeat()
        if not self.repeat:
            required = self.config.mode_minimum_multiplier.get(self.betmode)
            if required is not None and self.get_highest_multiplier() < required:
                self.repeat = True
