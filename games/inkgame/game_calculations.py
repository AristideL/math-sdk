"""Scatter pays game calculations"""

from src.executables.executables import Executables


class GameCalculations(Executables):
    """Game specific calculations for Scatter sample game."""

    def get_board_multipliers(self, multiplier_key: str = "multiplier") -> list:
        """Find multiplier from board using winning positions."""
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

    def get_highest_multiplier(self, multiplier_key: str = "multiplier") -> int:
        """Get the highest multiplier value on the board."""
        max_mult = 0
        for reel, _ in enumerate(self.board):
            for row, _ in enumerate(self.board[reel]):
                if self.board[reel][row].check_attribute(multiplier_key):
                    mult_value = self.board[reel][row].get_attribute(multiplier_key)
                    if mult_value > max_mult:
                        max_mult = mult_value
        return max_mult

    def enforce_multiplier_guarantee(self):
        """Enforce minimum multiplier guarantees for single-spin modes.
        
        This method is called after board generation to ensure that:
        - Single-spin modes (min_one_x10, min_one_x100, min_one_x1000) have at least one M symbol
        - The M symbol has a multiplier >= the required minimum
        """
        cond = self.get_current_distribution_conditions() or {}
        required_min = cond.get("guaranteed_min_bomb")
        
        if required_min is None:
            return
        
        # Check if this is a single-spin mode
        if not cond.get("single_spin_feature"):
            return
        
        # Check if we already have an M symbol with sufficient multiplier
        highest = self.get_highest_multiplier()
        if highest >= required_min:
            # Make sure the flag is set
            self.guaranteed_min_bomb_seen = True
            return
        
        # Need to place/upgrade an M symbol
        # Find all M symbols on board
        m_positions = []
        for reel, _ in enumerate(self.board):
            for row, _ in enumerate(self.board[reel]):
                if self.board[reel][row].name == "M":
                    m_positions.append((reel, row))
        
        if m_positions:
            # Upgrade one existing M to meet the requirement
            reel, row = m_positions[0]
            self.board[reel][row].assign_attribute({"multiplier": required_min})
            self.guaranteed_min_bomb_seen = True
        else:
            # Place a new M symbol on a random valid position
            import random
            valid_spots = []
            for reel, _ in enumerate(self.board):
                for row, _ in enumerate(self.board[reel]):
                    # Don't replace scatter symbols
                    if self.board[reel][row].name not in ["S"]:
                        valid_spots.append((reel, row))
            
            if valid_spots:
                reel, row = random.choice(valid_spots)
                # Replace with M symbol - create it with the exact multiplier needed
                m_symbol = self.create_symbol("M")
                # Override whatever multiplier was assigned to ensure we have the minimum
                m_symbol.assign_attribute({"multiplier": required_min})
                self.board[reel][row] = m_symbol
                # Update special symbols tracking
                self.get_special_symbols_on_board()
                # Mark that we've fulfilled the guarantee
                self.guaranteed_min_bomb_seen = True
