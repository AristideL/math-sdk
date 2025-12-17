"""Validation script for Boring Job 1000 bet modes.

This script validates that all bet modes work correctly:
- base: No M symbols on board
- bonus: Buy bonus with multipliers in freegame
- doubleboost: Double chance to trigger bonus
- no_small_bomb: No multipliers < 10 in freegame
- min_one_x10: At least one M with mult >= 10
- min_one_x100: At least one M with mult >= 100
- min_one_x1000: At least one M with mult >= 1000
"""

import sys
sys.path.insert(0, '.')

from game_config import GameConfig
from gamestate import GameState


def validate_base_mode(gamestate, config):
    """Validate that base mode never has M symbols on initial board."""
    print("\n=== Validating BASE mode ===")
    gamestate.betmode = "base"
    gamestate.criteria = "basegame"
    gamestate.gametype = config.basegame_type
    
    # Test 10 random boards
    has_m_count = 0
    for i in range(10):
        gamestate.reset_book()
        gamestate.draw_board(emit_event=False)
        gamestate.enforce_multiplier_guarantee()
        
        # Count M symbols
        m_count = 0
        for reel in gamestate.board:
            for cell in reel:
                if cell.name == "M":
                    m_count += 1
        
        if m_count > 0:
            has_m_count += 1
    
    if has_m_count == 0:
        print("✓ PASS: Base mode has no M symbols on board (tested 10 boards)")
        return True
    else:
        print(f"✗ FAIL: Base mode had M symbols on {has_m_count}/10 boards")
        return False


def validate_single_spin_mode(gamestate, config, mode_name, min_mult):
    """Validate single-spin modes guarantee at least one M with minimum multiplier."""
    print(f"\n=== Validating {mode_name.upper()} mode ===")
    gamestate.betmode = mode_name
    
    # Test both criteria
    for criteria in ["0", "basegame"]:
        gamestate.criteria = criteria
        gamestate.gametype = config.basegame_type
        
        # Test 10 random boards
        failures = []
        for i in range(10):
            gamestate.reset_book()
            gamestate.draw_board(emit_event=False)
            gamestate.enforce_multiplier_guarantee()
            
            # Check for M symbols and multipliers
            m_count = 0
            max_mult = 0
            for reel in gamestate.board:
                for cell in reel:
                    if cell.name == "M":
                        m_count += 1
                        if cell.check_attribute("multiplier"):
                            mult = cell.get_attribute("multiplier")
                            max_mult = max(max_mult, mult)
            
            if m_count == 0:
                failures.append(f"Trial {i}: No M symbols")
            elif max_mult < min_mult:
                failures.append(f"Trial {i}: Max mult {max_mult} < {min_mult}")
        
        if len(failures) == 0:
            print(f"✓ PASS: {mode_name} ({criteria}) always has M with mult >= {min_mult} (tested 10 boards)")
        else:
            print(f"✗ FAIL: {mode_name} ({criteria}) had {len(failures)} failures:")
            for f in failures[:3]:  # Show first 3 failures
                print(f"  {f}")
            return False
    
    return True


def validate_no_small_bomb_mode(gamestate, config):
    """Validate that no_small_bomb mode filters multipliers < 10 in freegame."""
    print("\n=== Validating NO_SMALL_BOMB mode ===")
    gamestate.betmode = "no_small_bomb"
    gamestate.criteria = "freegame"
    gamestate.gametype = config.freegame_type  # In freegame context
    
    # Test 10 random boards
    small_bomb_count = 0
    for i in range(10):
        gamestate.reset_book()
        gamestate.draw_board(emit_event=False)
        
        # Check all M symbols
        for reel in gamestate.board:
            for cell in reel:
                if cell.name == "M" and cell.check_attribute("multiplier"):
                    mult = cell.get_attribute("multiplier")
                    if mult < 10:
                        small_bomb_count += 1
                        print(f"  Found bomb with mult={mult} < 10 on trial {i}")
    
    if small_bomb_count == 0:
        print("✓ PASS: no_small_bomb mode has no multipliers < 10 (tested 10 boards)")
        return True
    else:
        print(f"✗ FAIL: no_small_bomb mode had {small_bomb_count} multipliers < 10")
        return False


def validate_bonus_mode(gamestate, config):
    """Validate that bonus mode works correctly."""
    print("\n=== Validating BONUS mode ===")
    gamestate.betmode = "bonus"
    gamestate.criteria = "freegame"
    gamestate.gametype = config.freegame_type
    
    # Just test that it can generate boards
    try:
        for i in range(5):
            gamestate.reset_book()
            gamestate.draw_board(emit_event=False)
        print("✓ PASS: Bonus mode generates boards successfully")
        return True
    except Exception as e:
        print(f"✗ FAIL: Bonus mode failed: {e}")
        return False


def validate_doubleboost_mode(gamestate, config):
    """Validate that doubleboost mode works correctly."""
    print("\n=== Validating DOUBLEBOOST mode ===")
    gamestate.betmode = "doubleboost"
    gamestate.criteria = "basegame"
    gamestate.gametype = config.basegame_type
    
    # Just test that it can generate boards
    try:
        for i in range(5):
            gamestate.reset_book()
            gamestate.draw_board(emit_event=False)
        print("✓ PASS: Doubleboost mode generates boards successfully")
        return True
    except Exception as e:
        print(f"✗ FAIL: Doubleboost mode failed: {e}")
        return False


def main():
    """Run all validations."""
    config = GameConfig()
    gamestate = GameState(config)
    
    print("=" * 60)
    print("Boring Job 1000 - Mode Validation")
    print("=" * 60)
    
    results = []
    
    # Validate each mode
    results.append(("base", validate_base_mode(gamestate, config)))
    results.append(("bonus", validate_bonus_mode(gamestate, config)))
    results.append(("doubleboost", validate_doubleboost_mode(gamestate, config)))
    results.append(("no_small_bomb", validate_no_small_bomb_mode(gamestate, config)))
    results.append(("min_one_x10", validate_single_spin_mode(gamestate, config, "min_one_x10", 10)))
    results.append(("min_one_x100", validate_single_spin_mode(gamestate, config, "min_one_x100", 100)))
    results.append(("min_one_x1000", validate_single_spin_mode(gamestate, config, "min_one_x1000", 1000)))
    
    # Summary
    print("\n" + "=" * 60)
    print("VALIDATION SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for mode, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {mode}")
    
    print(f"\nTotal: {passed}/{total} modes passed")
    
    if passed == total:
        print("\n🎉 All validations passed!")
        return 0
    else:
        print(f"\n❌ {total - passed} validation(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
