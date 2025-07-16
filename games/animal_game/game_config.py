"""Template game configuration file, detailing required user-specified inputs."""

from src.config.config import Config
from src.config.distributions import Distribution
from src.config.config import BetMode


class GameConfig(Config):
    """Template configuration class."""

    def __init__(self):
        super().__init__()
        self.game_id = "animal_game"
        self.provider_numer = 0
        self.working_name = "animal_game"
        self.wincap = 300
        self.win_type = "other"
        self.rtp = 0.96
        self.construct_paths()

        # Game Dimensions
        self.num_reels = 3
        self.num_rows = [3] * self.num_reels  # Optionally include variable number of rows per reel
        # Board and Symbol Properties
        self.paytable = {
            (3, "T1"): 100,
            (3, "T2"): 50,
            (3, "T3"): 10,
            (3, "L1"): 5.0,
            (3, "L2"): 2.0,
            (3, "L3"): 0.5,
        }
        self.sym_dist = {"T1": 2, "T2": 100, "T3": 200, "L1": 400, "L2": 600, "L3": 700}

        self.include_padding = False
        self.special_symbols = {"wild": [], "scatter": [], "multiplier": []}

        self.freespin_triggers = {self.basegame_type: {}, self.freegame_type: {}}
        self.anticipation_triggers = {self.basegame_type: 0, self.freegame_type: 0}
        # Reels
        # reels = {"BR0": "BR0.csv", "FR0": "FR0.csv"}
        # self.reels = {}
        # for r, f in reels.items():
        #     self.reels[r] = self.read_reels_csv(str.join("/", [self.reels_path, f]))

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
                        },
                    ),
                    Distribution(
                        criteria="basegame",
                        quota=0.6,
                        conditions={
                            "reel_weights": {self.basegame_type: {"BR0": 1}},
                            "force_wincap": False,
                            "force_freegame": False,
                        },
                    ),
                    Distribution(
                        criteria="0",
                        quota=0.4,
                        conditions={
                            "reel_weights": {self.basegame_type: {"BR0": 1}},
                            "force_wincap": False,
                            "force_freegame": False,
                        },
                    ),
                ],
            ),
        ]
