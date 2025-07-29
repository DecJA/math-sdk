"""Template game configuration file, detailing required user-specified inputs."""

from src.config.config import Config
from src.config.distributions import Distribution
from src.config.config import BetMode


class GameConfig(Config):
    """Template configuration class."""

    def __init__(self):
        super().__init__()
        self.game_id = "mega_mutis"
        self.provider_numer = 0
        self.working_name = "mega_mutis"
        self.wincap = 5000
        self.win_type = "other"
        self.rtp = 0.96
        self.construct_paths()

        # Game Dimensions
        self.num_reels = 3
        self.num_rows = [3] * self.num_reels  # Optionally include variable number of rows per reel
        # Board and Symbol Properties
        self.paytable = {(10, "P"): 0}
        self.prize_range = {"base": [0, 5000]}
        self.prize_dist = {
            0.2: 900,
            0.5: 830,
            0.7: 500,
            1.0: 200,
            2.0: 100,
            5.0: 50,
            10: 20,
            20: 10,
            50: 10,
            100: 5,
            500: 4,
            1000: 3,
            5000: 2,
        }
        self.bonus_dist = {
            5: 300,
            10: 350,
            15: 400,
            25: 500,
            50: 550,
            75: 400,
            100: 300,
            200: 200,
            500: 120,
            1000: 10,
            2000: 3,
            5000: 5,
        }

        self.num_dummy_placement = {1: 30, 2: 10}
        self.padding_dist = {
            50: 500,
            75: 400,
            100: 300,
            200: 200,
            500: 100,
            1000: 50,
            2000: 20,
            5000: 15,
        }

        self.include_padding = False
        self.special_symbols = {"prize": ["P"], "scatter": [], "multiplier": []}

        self.freespin_triggers = {self.basegame_type: {}, self.freegame_type: {}}
        self.anticipation_triggers = {self.basegame_type: 0, self.freegame_type: 0}
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
                        conditions={
                            "reel_weights": {self.basegame_type: {"BR0": 1}},
                            "force_wincap": True,
                            "force_freegame": False,
                            "prize_dist": self.prize_dist,
                        },
                    ),
                    Distribution(
                        criteria="basegame",
                        quota=0.6,
                        conditions={
                            "reel_weights": {self.basegame_type: {"BR0": 1}},
                            "force_wincap": False,
                            "force_freegame": False,
                            "prize_dist": self.prize_dist,
                        },
                    ),
                    Distribution(
                        criteria="0",
                        quota=0.4,
                        conditions={
                            "reel_weights": {self.basegame_type: {"BR0": 1}},
                            "force_wincap": False,
                            "force_freegame": False,
                            "prize_dist": self.prize_dist,
                        },
                    ),
                ],
            ),
            BetMode(
                name="bonus",
                cost=100.0,
                rtp=self.rtp,
                max_win=self.wincap,
                auto_close_disabled=False,
                is_feature=True,
                is_buybonus=False,
                distributions=[
                    Distribution(
                        criteria="wincap",
                        quota=0.001,
                        conditions={
                            "reel_weights": {self.basegame_type: {"BR0": 1}},
                            "force_wincap": True,
                            "force_freegame": False,
                            "prize_dist": self.bonus_dist,
                        },
                    ),
                    Distribution(
                        criteria="basegame",
                        quota=0.6,
                        conditions={
                            "reel_weights": {self.basegame_type: {"BR0": 1}},
                            "force_wincap": False,
                            "force_freegame": False,
                            "prize_dist": self.bonus_dist,
                        },
                    ),
                ],
            ),
        ]
