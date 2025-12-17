from game_override import GameStateOverride
from src.calculations.scatter import Scatter


class GameState(GameStateOverride):
    """Gamestate for a single spin"""
    
    def _board_has_M(self):
        for row in self.board:
            for cell in row:
                if getattr(cell, "symbol", None) == "M":
                    return True
        return False

    def _force_place_one_M(self):
        from random import choice
        spots = [(r,c) for r,row in enumerate(self.board)
                       for c,cell in enumerate(row)
                       if getattr(cell, "symbol", None) not in ("SCATTER","BLOCK")]
        if spots:
            r,c = choice(spots)
            self.assign_mult_property(self.board[r][c])
        else:
            print("Warning: No valid spot to place M symbol!")

    def run_spin(self, sim: int):
        self.reset_seed(sim)
        self.repeat = True
        while self.repeat:
            self.reset_book()
            self.draw_board()
            # if self._is_single_spin_mode() and not self._board_has_M():
            #     self._force_place_one_M()

            self.get_scatterpays_update_wins()
            self.emit_tumble_win_events()  # Transmit win information

            while self.win_data["totalWin"] > 0 and not (self.wincap_triggered):
                self.tumble_game_board()
                self.get_scatterpays_update_wins()

            self.set_end_tumble_event()
            self.win_manager.update_gametype_wins(self.gametype)

            if self.check_fs_condition() and self.check_freespin_entry():
                self.run_freespin_from_base()

            self.evaluate_finalwin()
            self.check_repeat()

        self.imprint_wins()

    def run_freespin(self):
        self.reset_fs_spin()
        while self.fs < self.tot_fs:
            # Resets global multiplier at each spin
            self.update_freespin()
            self.draw_board()

            self.get_scatterpays_update_wins()
            self.emit_tumble_win_events()  # Transmit win information

            while self.win_data["totalWin"] > 0 and not (self.wincap_triggered):
                # Tumble/cascade. No global multiplier growth in bonus.
                self.tumble_game_board()
                self.get_scatterpays_update_wins()

            self.set_end_tumble_event()
            self.win_manager.update_gametype_wins(self.gametype)

            if self.check_fs_condition():
                self.update_fs_retrigger_amt()

        self.end_freespin()
