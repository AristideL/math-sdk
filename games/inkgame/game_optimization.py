"""Set conditions/parameters for optimization program program"""

from optimization_program.optimization_config import (
    ConstructScaling,
    ConstructParameters,
    ConstructConditions,
    verify_optimization_input,
)


class OptimizationSetup:
    """Handle all game mode optimization parameters."""

    def __init__(self, game_config):
        self.game_config = game_config
        self.game_config.opt_params = {
            "base": {
                "conditions": {
                    "wincap": ConstructConditions(
                        rtp=0.01, av_win=25000, search_conditions=25000
                    ).return_dict(),
                    "0": ConstructConditions(
                        rtp=0, av_win=0, search_conditions=0
                    ).return_dict(),
                    "freegame": ConstructConditions(
                        rtp=0.37, hr=200, search_conditions={"symbol": "scatter"}
                    ).return_dict(),
                    "basegame": ConstructConditions(hr=3.5, rtp=0.585).return_dict(),
                },
                "scaling": ConstructScaling(
                    [
                        {
                            "criteria": "basegame",
                            "scale_factor": 1.2,
                            "win_range": (1, 2),
                            "probability": 1.0,
                        },
                        {
                            "criteria": "basegame",
                            "scale_factor": 1.5,
                            "win_range": (10, 20),
                            "probability": 1.0,
                        },
                        {
                            "criteria": "freegame",
                            "scale_factor": 0.8,
                            "win_range": (1000, 2000),
                            "probability": 1.0,
                        },
                        {
                            "criteria": "freegame",
                            "scale_factor": 1.2,
                            "win_range": (3000, 4000),
                            "probability": 1.0,
                        },
                    ]
                ).return_dict(),
                "parameters": ConstructParameters(
                    num_show=5000,
                    num_per_fence=10000,
                    min_m2m=4,
                    max_m2m=8,
                    pmb_rtp=1.0,
                    sim_trials=5000,
                    test_spins=[50, 100, 200],
                    test_weights=[0.3, 0.4, 0.3],
                    score_type="rtp",
                ).return_dict(),
            },
            "bonus": {
                "conditions": {
                    "wincap": ConstructConditions(
                        rtp=0.01, av_win=25000, search_conditions=25000
                    ).return_dict(),
                    "freegame": ConstructConditions(rtp=0.955, hr="x").return_dict(),
                },
                "scaling": ConstructScaling(
                    [
                        {
                            "criteria": "freegame",
                            "scale_factor": 0.9,
                            "win_range": (20, 50),
                            "probability": 1.0,
                        },
                        {
                            "criteria": "freegame",
                            "scale_factor": 0.8,
                            "win_range": (1000, 2000),
                            "probability": 1.0,
                        },
                        {
                            "criteria": "freegame",
                            "scale_factor": 1.2,
                            "win_range": (3000, 4000),
                            "probability": 1.0,
                        },
                    ]
                ).return_dict(),
                "parameters": ConstructParameters(
                    num_show=5000,
                    num_per_fence=10000,
                    min_m2m=4,
                    max_m2m=8,
                    pmb_rtp=1.0,
                    sim_trials=5000,
                    test_spins=[10, 20, 50],
                    test_weights=[0.6, 0.2, 0.2],
                    score_type="rtp",
                ).return_dict(),
            },
            "doubleboost": {
                "conditions": {
                    "wincap": ConstructConditions(
                        rtp=0.01, av_win=25000, search_conditions=25000
                    ).return_dict(),
                    "0": ConstructConditions(
                        rtp=0, av_win=0, search_conditions=0
                    ).return_dict(),
                    # +8 pts de RTP vers freegame vs "base" (0.37 -> 0.45) pour refléter le double chance
                    "freegame": ConstructConditions(
                        rtp=0.45, hr=180, search_conditions={"symbol": "scatter"}
                    ).return_dict(),
                    # Basegame réduit pour conserver RTP total = 0.965
                    "basegame": ConstructConditions(rtp=0.505, hr=3.2).return_dict(),
                },
                "scaling": ConstructScaling(
                    [
                        {
                            "criteria": "basegame",
                            "scale_factor": 1.2,
                            "win_range": (1, 2),
                            "probability": 1.0,
                        },
                        {
                            "criteria": "basegame",
                            "scale_factor": 1.5,
                            "win_range": (10, 20),
                            "probability": 1.0,
                        },
                        {
                            "criteria": "freegame",
                            "scale_factor": 0.85,
                            "win_range": (200, 600),
                            "probability": 1.0,
                        },
                        {
                            "criteria": "freegame",
                            "scale_factor": 1.15,
                            "win_range": (1500, 3000),
                            "probability": 1.0,
                        },
                    ]
                ).return_dict(),
                "parameters": ConstructParameters(
                    num_show=5000,
                    num_per_fence=10000,
                    min_m2m=4,
                    max_m2m=8,
                    pmb_rtp=1.0,
                    sim_trials=5000,
                    test_spins=[50, 100, 200],
                    test_weights=[0.3, 0.4, 0.3],
                    score_type="rtp",
                ).return_dict(),
            },
            "min_one_x10": {
                "conditions": {
                    "0": ConstructConditions(
                        rtp=0, av_win=0, search_conditions={"symbol": "multiplier"}
                    ).return_dict(),
                    "basegame": ConstructConditions(
                        hr=3.0, rtp=0.965,search_conditions={"symbol": "multiplier"}
                    ).return_dict(),  # basegame ici
                },
                "scaling": ConstructScaling(
    [
        {
            "criteria": "basegame",
            "scale_factor": 0.90,
            "win_range": (0, 20),
            "probability": 1.0,
        },
        {
            "criteria": "basegame",
            "scale_factor": 0.95,
            "win_range": (20, 80),
            "probability": 1.0,
        },
        {
            "criteria": "basegame",
            "scale_factor": 1.00,
            "win_range": (80, 200),
            "probability": 1.0,
        },
        {
            "criteria": "basegame",
            "scale_factor": 1.05,
            "win_range": (200, 600),
            "probability": 1.0,
        },
        {
            "criteria": "basegame",
            "scale_factor": 1.10,
            "win_range": (600, 1200),
            "probability": 1.0,
        },
        {
            "criteria": "basegame",
            "scale_factor": 1.20,
            "win_range": (1200, 999999),
            "probability": 1.0,
        },
    ]
).return_dict(),

                "parameters": ConstructParameters(
                    num_show=5000,
                    num_per_fence=10000,
                    min_m2m=4,
                    max_m2m=8,
                    pmb_rtp=1.0,
                    sim_trials=5000,
                    test_spins=[10, 20, 50],
                    test_weights=[0.6, 0.2, 0.2],
                    score_type="rtp",
                ).return_dict(),
            },
            # Buy bonus 200x : même enveloppe RTP que "bonus", mais cible au moins une bombe x100
            "min_one_x100": {
                "conditions": {
                    "0": ConstructConditions(
                        rtp=0, av_win=0,search_conditions={"symbol": "multiplier"}
                    ).return_dict(),
                    "basegame": ConstructConditions(
                        hr=3.0, rtp=0.965,search_conditions={"symbol": "multiplier"}
                    ).return_dict(),  # basegame ici
                },
                "scaling": ConstructScaling(
    [
        {
            "criteria": "basegame",
            "scale_factor": 0.90,
            "win_range": (0, 20),
            "probability": 1.0,
        },
        {
            "criteria": "basegame",
            "scale_factor": 0.95,
            "win_range": (20, 80),
            "probability": 1.0,
        },
        {
            "criteria": "basegame",
            "scale_factor": 1.00,
            "win_range": (80, 200),
            "probability": 1.0,
        },
        {
            "criteria": "basegame",
            "scale_factor": 1.05,
            "win_range": (200, 600),
            "probability": 1.0,
        },
        {
            "criteria": "basegame",
            "scale_factor": 1.10,
            "win_range": (600, 1200),
            "probability": 1.0,
        },
        {
            "criteria": "basegame",
            "scale_factor": 1.20,
            "win_range": (1200, 999999),
            "probability": 1.0,
        },
    ]
).return_dict(),

                "parameters": ConstructParameters(
                    num_show=5000,
                    num_per_fence=10000,
                    min_m2m=4,
                    max_m2m=8,
                    pmb_rtp=1.0,
                    sim_trials=5000,
                    test_spins=[10, 20, 50],
                    test_weights=[0.6, 0.2, 0.2],
                    score_type="rtp",
                ).return_dict(),
            },
            # Buy bonus 350x : cible au moins une bombe x1000
            "min_one_x1000": {
                "conditions": {
                    "0": ConstructConditions(
                        rtp=0, av_win=0,search_conditions={"symbol": "multiplier"}
                    ).return_dict(),
                    "basegame": ConstructConditions(hr=3.5, rtp=0.965,search_conditions={"symbol": "multiplier"}).return_dict(),
                },
                "scaling": ConstructScaling(
    [
        {
            "criteria": "basegame",
            "scale_factor": 0.90,
            "win_range": (0, 20),
            "probability": 1.0,
        },
        {
            "criteria": "basegame",
            "scale_factor": 0.95,
            "win_range": (20, 80),
            "probability": 1.0,
        },
        {
            "criteria": "basegame",
            "scale_factor": 1.00,
            "win_range": (80, 200),
            "probability": 1.0,
        },
        {
            "criteria": "basegame",
            "scale_factor": 1.05,
            "win_range": (200, 600),
            "probability": 1.0,
        },
        {
            "criteria": "basegame",
            "scale_factor": 1.10,
            "win_range": (600, 1200),
            "probability": 1.0,
        },
        {
            "criteria": "basegame",
            "scale_factor": 1.20,
            "win_range": (1200, 999999),
            "probability": 1.0,
        },
    ]
).return_dict(),

                "parameters": ConstructParameters(
                    num_show=5000,
                    num_per_fence=12000,
                    min_m2m=4,
                    max_m2m=8,
                    pmb_rtp=1.0,
                    sim_trials=6000,
                    test_spins=[10, 20, 50],
                    test_weights=[0.6, 0.2, 0.2],
                    score_type="rtp",
                ).return_dict(),
            },
            # Buy bonus 500x : supprime les petites bombes (<x10)
            "no_small_bomb": {
                "conditions": {
                    "freegame": ConstructConditions(rtp=0.965, hr="x").return_dict(),
                },
                "scaling": ConstructScaling(
                    [
                        {
                            "criteria": "freegame",
                            "scale_factor": 1.05,
                            "win_range": (50, 150),
                            "probability": 1.0,
                        },
                        {
                            "criteria": "freegame",
                            "scale_factor": 0.9,
                            "win_range": (300, 900),
                            "probability": 1.0,
                        },
                        {
                            "criteria": "freegame",
                            "scale_factor": 1.15,
                            "win_range": (1500, 3000),
                            "probability": 1.0,
                        },
                        {
                            "criteria": "freegame",
                            "scale_factor": 1.05,
                            "win_range": (4000, 6000),
                            "probability": 1.0,
                        },
                    ]
                ).return_dict(),
                "parameters": ConstructParameters(
                    num_show=5000,
                    num_per_fence=12000,
                    min_m2m=4,
                    max_m2m=8,
                    pmb_rtp=1.0,
                    sim_trials=6000,
                    test_spins=[10, 20, 50],
                    test_weights=[0.6, 0.2, 0.2],
                    score_type="rtp",
                ).return_dict(),
            },
        }

        verify_optimization_input(self.game_config, self.game_config.opt_params)
