from game_executables import *
from src.events.events import update_freespin_event, update_global_mult_event
from src.calculations.statistics import get_random_outcome


class GameStateOverride(GameExecutables):
    def reset_book(self):
        super().reset_book()
        self.tumble_win = 0
        self.guaranteed_min_bomb_seen = False
        self.freegame_finished = False

    def reset_fs_spin(self):
        super().reset_fs_spin()
        self.global_multiplier = 1
        self.guaranteed_min_bomb_seen = False

    def assign_special_sym_function(self):
        self.special_symbol_functions = {"M": [self.assign_mult_property]}

    def _is_single_spin_mode(self):
        cond = self.get_current_distribution_conditions() or {}
        return bool(cond.get("single_spin_feature"))

    def _is_end_of_freegame(self):
        if hasattr(self, "fs_remaining"):
            return self.fs_remaining == 0
        if hasattr(self, "fs_spins_played") and hasattr(self, "fs_total_spins"):
            return self.fs_spins_played >= self.fs_total_spins
        return bool(getattr(self, "freegame_finished", False))
    
    def _required_min_bomb(self, cond):
        if self._is_single_spin_mode():
            return cond.get("guaranteed_min_bomb")
        return cond.get("guaranteed_min_bomb")

    def assign_mult_property(self, symbol):
        cond = self.get_current_distribution_conditions() or {}
        in_freegame = self.gametype == self.config.freegame_type
        if not (in_freegame or self._is_single_spin_mode()):
            return

        mv = cond.get("mult_values", {}) or {}
        table = mv.get(self.gametype, mv.get(self.config.freegame_type, {})) or {}
        need = self._required_min_bomb(cond)
        # print(f"Assigning multiplier, need: {need}, table: {table}")

        # Optionnel: si la table ne permet pas d'atteindre 'need', on l'autorise
        if need is not None and not any(m >= need for m in table):
            table = {**table, need: 1}

        min_req = cond.get("min_bomb_mult")
        if min_req is not None:
            table = {m: w for m, w in table.items() if m >= min_req} or table

        value = get_random_outcome(table)
        if value is None:
            return
        symbol.assign_attribute({"multiplier": value})
        if need is not None and value == need:
            self.guaranteed_min_bomb_seen = True
        # print(f"Multiplier assigned: {value}, guaranteed_min_bomb_seen: {self.guaranteed_min_bomb_seen}")

    def set_end_tumble_event(self):
        """Applique le board multiplier en freegame OU en mode 1-spin."""
        apply_mult = (self.gametype == self.config.freegame_type) or self._is_single_spin_mode()
        if apply_mult:
            board_mult, mult_info = self.get_board_multipliers()
            base_tumble_win = copy(self.win_manager.spin_win)
            self.win_manager.set_spin_win(base_tumble_win * board_mult)
            if self.win_manager.spin_win > 0 and len(mult_info) > 0:
                send_mult_info_event(self, board_mult, mult_info, base_tumble_win, self.win_manager.spin_win)
                update_tumble_win_event(self)

        if self.win_manager.spin_win > 0:
            set_win_event(self)
        set_total_event(self)

    def check_game_repeat(self):
        if self.repeat:
            return
        win_criteria = self.get_current_betmode_distributions().get_win_criteria()
        if win_criteria is not None and self.final_win != win_criteria:
            self.repeat = True
            return

        cond = self.get_current_distribution_conditions() or {}
        need = self._required_min_bomb(cond)
        if need is None:
            return

        if self._is_single_spin_mode():
            if not self.guaranteed_min_bomb_seen:
                self.repeat = True
            return

        if self.gametype == self.config.freegame_type and self._is_end_of_freegame():
            if not self.guaranteed_min_bomb_seen:
                self.repeat = True
