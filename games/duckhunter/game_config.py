import os
from src.config.config import Config
from src.config.distributions import Distribution
from src.config.betmode import BetMode
from src.config.paths import PROJECT_PATH


class GameConfig(Config):
    """Load all game specific parameters and elements"""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        os.chdir(PROJECT_PATH)
        super().__init__()
        self.game_id = "0_0_scatter"
        self.game_name = "sample_scatter"
        self.provider_numer = 0
        self.working_name = "Sample scatter pay (pay anywhere)"
        self.wincap = 5000.0
        self.win_type = "scatter"
        self.rtp = 0.9600
        self.construct_paths()

        # Game Dimensions
        self.num_reels = 5
        self.num_rows = [1] * self.num_reels  # Optionally include variable number of rows per reel
        # Board and Symbol Properties
        pay_range = {
            "B1": (0, 1.0),
            "B2": (1.0, 10.0),
            "B3": (10.0, 50.0),
            "B4": (50.0, 500.0),
            "B5": (500.0, 1000.0),
        }

        self.paytable = pay_range

        self.num_display_birds = 5

        self.bird_selection = {
            self.basegame_type: {
                "B1": 1000,
                "B2": 500,
                "B3": 200,
                "B4": 50,
                "B5": 20,
                "RD": 5,
            },
            self.freegame_type: {
                "B2": 500,
                "B3": 200,
                "B4": 50,
                "B5": 20,
                "RD": 5,
            },
        }

        self.include_padding = True
        self.special_symbols = {"scatter": ["RD"], "multiplier": []}

        self.freespin_triggers = {
            self.basegame_type: {1: 3},
            self.freegame_type: {1: 3},
        }
        self.anticipation_triggers = {
            self.basegame_type: float("inf"),
            self.freegame_type: float("inf"),
        }
        # Reels
        self.reels = {}
        # for r, f in reels.items():
        #     self.reels[r] = self.read_reels_csv(os.path.join(self.reels_path, f))

        self.padding_reels[self.basegame_type] = self.reels["BR0"]
        self.padding_reels[self.freegame_type] = self.reels["FR0"]
        self.bet_modes = [
            BetMode(
                name="base",
                cost=1.0,
                rtp=self.rtp,
                max_win=self.wincap,
                auto_close_disabled=False,
                is_feature=True,
                is_buybonus=False,
                distributions=[
                    Distribution(
                        criteria="wincap",
                        quota=0.001,
                        win_criteria=self.wincap,
                        conditions={
                            "reel_weights": {
                                self.basegame_type: {"BR0": 1},
                                self.freegame_type: {"FR0": 1},
                            },
                            "scatter_triggers": {1: 1},
                            "force_wincap": True,
                            "force_freegame": True,
                        },
                    ),
                    Distribution(
                        criteria="freegame",
                        quota=0.1,
                        conditions={
                            "reel_weights": {
                                self.basegame_type: {"BR0": 1},
                                self.freegame_type: {"FR0": 1},
                            },
                            "scatter_triggers": {1: 1},
                            "force_wincap": False,
                            "force_freegame": True,
                        },
                    ),
                    Distribution(
                        criteria="0",
                        quota=0.4,
                        win_criteria=0.0,
                        conditions={
                            "reel_weights": {self.basegame_type: {"BR0": 1}},
                            "force_wincap": False,
                            "force_freegame": False,
                        },
                    ),
                    Distribution(
                        criteria="basegame",
                        quota=0.5,
                        conditions={
                            "reel_weights": {self.basegame_type: {"BR0": 1}},
                            "force_wincap": False,
                            "force_freegame": False,
                        },
                    ),
                ],
            ),
            # BetMode(
            #     name="bonus",
            #     cost=200,
            #     rtp=self.rtp,
            #     max_win=self.wincap,
            #     auto_close_disabled=False,
            #     is_feature=False,
            #     is_buybonus=True,
            #     distributions=[
            #         Distribution(
            #             criteria="wincap",
            #             quota=0.001,
            #             # win_criteria=self.wincap,
            #             conditions={
            #                 "reel_weights": {
            #                     self.basegame_type: {"BR0": 1},
            #                     self.freegame_type: {"FR0": 1},
            #                 },
            #                 "mult_values": {
            #                     self.basegame_type: {2: 100, 4: 80, 5: 50, 7: 20, 10: 10},
            #                     self.freegame_type: {2: 100, 4: 80, 5: 50, 7: 20, 10: 10},
            #                 },
            #                 "scatter_triggers": {4: 10, 5: 5, 6: 1},
            #                 "force_wincap": True,
            #                 "force_freegame": True,
            #             },
            #         ),
            #         Distribution(
            #             criteria="freegame",
            #             quota=0.1,
            #             conditions={
            #                 "reel_weights": {
            #                     self.basegame_type: {"BR0": 1},
            #                     self.freegame_type: {"FR0": 1},
            #                 },
            #                 "scatter_triggers": {4: 10, 5: 5, 6: 1},
            #                 "mult_values": {
            #                     self.basegame_type: {2: 100, 4: 80, 5: 50, 7: 20, 10: 10},
            #                     self.freegame_type: {2: 100, 4: 80, 5: 50, 7: 20, 10: 10},
            #                 },
            #                 "force_wincap": False,
            #                 "force_freegame": True,
            #             },
            #         ),
            #     ],
            # ),
        ]
