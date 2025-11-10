import parser


class Loot(parser.CSVRow):
    ItemID: int
    Slot: str
    Quality: str
    BaseItemPower: int
    SellValue: int


class Equipment:
    weapon: int = 0
    helm: int = 0
    chest: int = 0
    legs: int = 0
    accessory: int = 0

    def get_score(self) -> int:
        return self.weapon + self.helm + self.chest + self.legs + self.accessory

    def equip_best(self, loot: list[Loot]):
        for l in loot:
            match l.Slot:
                case "Weapon":
                    self.weapon = max(self.weapon, l.BaseItemPower)
                case "Helm":
                    self.helm = max(self.helm, l.BaseItemPower)
                case "Chest":
                    self.chest = max(self.chest, l.BaseItemPower)
                case "Boots":
                    self.legs = max(self.legs, l.BaseItemPower)
                case _:
                    self.accessory = max(self.accessory, l.BaseItemPower)


class Progression(parser.CSVRow):
    Level: int
    XP_to_Next: int
    Gold_Combat: int
    Gold_NonCombat: int


class Player:
    _exp: int = 0
    level: int = 1

    _loot: list[Loot] = []
    equipment = Equipment()

    gold: int = 0

    _progression: list[Progression]

    def __init__(self):
        self._progression = parser.read_csv("data/Progression.csv", Progression)

    def get_exp(self, amount: int):
        self._exp += amount

        for p in self._progression:
            if p.Level == self.level:
                if self._exp >= p.XP_to_Next:
                    self.level += 1
                    self._exp -= p.XP_to_Next

    def get_loot(self, loot: Loot):
        self._loot.append(loot)
        self.equipment.equip_best(self._loot)


class Inputs:
    class Parameters:
        MaxLevel: int = 20
        BaseXPPerLevel: int = 100
        XPExponent: float = 1.35
        GoldPerCombatStep: int = 25
        GoldPerNonCombatStep: int = 10
        CombatChance: float = 0.6
        DeathChance: float = 0.08
        RepairCostPct: float = 0.05
        RespecChanceCombat: float = 0.03
        RespecBaseCost: float = 100
        RespecLevelMult: int = 10
        VendorTaxPct: float = 0.1
        ZoneTier: int = 1
        BaseXP_Combat: int = 12
        BaseXP_NonCombat: int = 10
        SkillDiff_TierMult: int = 5
        SkillDiff_StDev: int = 2
        TimePerStep_Min: int = 3
        DeathSeverity: float = 0.5
        RepairCostPerZone: float = 0.4
        StepCount: int = 20
        RunID: int = 1
        Seed: int = 1
        BaseRecommendedGear: int = 100
        GearGrowthPerZone: float = 1.08
        ZoneScale: int = 5
        GearStatScaling: int = 15


class World:
    BeatNum: int
    Stage: str
    BeatName: str
    BeatStartStep: int
    ZoneLevel: int
    BeatDC: int
