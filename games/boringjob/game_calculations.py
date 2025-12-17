"""Boringjob game calculations."""

from src.executables.executables import Executables
from src.calculations.scatter import Scatter


class GameCalculations(Executables):
    """Game specific calculations for boringjob."""

    def get_scatterpays_update_wins(self):
        """Evaluate scatter-style symbol wins and update wallet."""
        self.win_data = Scatter.get_scatterpay_wins(
            self.config, self.board, global_multiplier=self.global_multiplier
        )
        Scatter.record_scatter_wins(self)
        self.win_manager.tumble_win = self.win_data["totalWin"]
        self.win_manager.update_spinwin(self.win_data["totalWin"])

    def get_board_multipliers(self, multiplier_key: str = "multiplier") -> tuple:
        """Sum multipliers currently on the board."""
        board_mult = 0
        mult_info = []
        for reel, _ in enumerate(self.board):
            for row, _ in enumerate(self.board[reel]):
                if self.board[reel][row].check_attribute(multiplier_key):
                    board_mult += self.board[reel][row].get_attribute(multiplier_key)
                    mult_info.append(
                        {"reel": reel, "row": row, "value": self.board[reel][row].get_attribute(multiplier_key)}
                    )

        return max(1, board_mult), mult_info
