"""Quick simulation test for all modes."""

import sys
sys.path.insert(0, '.')

from game_config import GameConfig
from gamestate import GameState


def run_small_simulation(mode_name, num_sims=50):
    """Run a small simulation for a given mode."""
    config = GameConfig()
    gamestate = GameState(config)
    
    gamestate.betmode = mode_name
    mode = config.get_betmode(mode_name)
    
    print(f"\nTesting {mode_name} mode (cost={mode.get_cost()}):")
    
    wins = []
    for sim in range(num_sims):
        # Pick a distribution
        distributions = mode.get_distributions()
        gamestate.criteria = distributions[sim % len(distributions)].get_criteria()
        
        # Run the spin
        try:
            gamestate.run_spin(sim)
            wins.append(gamestate.final_win)
        except Exception as e:
            print(f"  ✗ Error on sim {sim}: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    # Basic stats
    total_win = sum(wins)
    avg_win = total_win / num_sims if num_sims > 0 else 0
    max_win = max(wins) if wins else 0
    non_zero = sum(1 for w in wins if w > 0)
    
    print(f"  ✓ {num_sims} spins completed")
    print(f"    Non-zero wins: {non_zero}/{num_sims} ({100*non_zero/num_sims:.1f}%)")
    print(f"    Avg win: {avg_win:.2f}x")
    print(f"    Max win: {max_win:.2f}x")
    
    return True


def main():
    """Run simulations for all modes."""
    modes = [
        "base",
        "bonus",
        "doubleboost",
        "no_small_bomb",
        "min_one_x10",
        "min_one_x100",
        "min_one_x1000",
    ]
    
    print("=" * 60)
    print("Quick Simulation Test - All Modes")
    print("=" * 60)
    
    results = []
    for mode in modes:
        success = run_small_simulation(mode, num_sims=50)
        results.append((mode, success))
    
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    
    for mode, success in results:
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"{status}: {mode}")
    
    all_pass = all(success for _, success in results)
    if all_pass:
        print("\n🎉 All modes simulated successfully!")
        return 0
    else:
        print("\n❌ Some modes failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
