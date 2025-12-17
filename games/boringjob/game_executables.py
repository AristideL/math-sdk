"""Executables for boringjob."""

try:
    from game_calculations import GameCalculations
except ModuleNotFoundError:  # pragma: no cover - support package import
    from games.boringjob.game_calculations import GameCalculations
from src.events.events import (
    win_info_event,
    set_win_event,
    set_total_event,
    update_tumble_win_event,
)


class GameExecutables(GameCalculations):
    """Executable helpers for boringjob."""

    def evaluate_boringjob_board(self):
        """Compute wins for current board."""
        self.get_scatterpays_update_wins()
        # Events are emitted via emit_tumble_win_events

    def set_end_tumble_event(self):
        """Apply multiplier symbols at the end of a tumble chain."""
        if self.win_manager.spin_win > 0:
            board_mult, _ = self.get_board_multipliers()
            base_tumble_win = self.win_manager.spin_win
            self.win_manager.set_spin_win(base_tumble_win * board_mult)
            if board_mult > 1:
                update_tumble_win_event(self)
            self.evaluate_wincap()
            set_win_event(self)
        set_total_event(self)
