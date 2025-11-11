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

        def __init__(self, data) -> None:
            self.MaxLevel = data.get('MaxLevel', self.MaxLevel)
            self.BaseXPPerLevel = data.get('BaseXPPerLevel', self.BaseXPPerLevel)
            self.XPExponent = data.get('XPExponent', self.XPExponent)
            self.GoldPerCombatStep = data.get('GoldPerCombatStep', self.GoldPerCombatStep)
            self.GoldPerNonCombatStep = data.get('GoldPerNonCombatStep', self.GoldPerNonCombatStep)
            self.CombatChance = data.get('CombatChance', self.CombatChance)
            self.DeathChance = data.get('DeathChance', self.DeathChance)
            self.RepairCostPct = data.get('RepairCostPct', self.RepairCostPct)
            self.RespecChanceCombat = data.get('RespecChanceCombat', self.RespecChanceCombat)
            self.RespecBaseCost = data.get('RespecBaseCost', self.RespecBaseCost)
            self.RespecLevelMult = data.get('RespecLevelMult', self.RespecLevelMult)
            self.VendorTaxPct = data.get('VendorTaxPct', self.VendorTaxPct)
            self.ZoneTier = data.get('ZoneTier', self.ZoneTier)
            self.BaseXP_Combat = data.get('BaseXP_Combat', self.BaseXP_Combat)
            self.BaseXP_NonCombat = data.get('BaseXP_NonCombat', self.BaseXP_NonCombat)
            self.SkillDiff_TierMult = data.get('SkillDiff_TierMult', self.SkillDiff_TierMult)
            self.SkillDiff_StDev = data.get('SkillDiff_StDev', self.SkillDiff_StDev)
            self.TimePerStep_Min = data.get('TimePerStep_Min', self.TimePerStep_Min)
            self.DeathSeverity = data.get('DeathSeverity', self.DeathSeverity)
            self.RepairCostPerZone = data.get('RepairCostPerZone', self.RepairCostPerZone)
            self.StepCount = data.get('StepCount', self.StepCount)
            self.RunID = data.get('RunID', self.RunID)
            self.Seed = data.get('Seed', self.Seed)
            self.BaseRecommendedGear = data.get('BaseRecommendedGear', self.BaseRecommendedGear)
            self.GearGrowthPerZone = data.get('GearGrowthPerZone', self.GearGrowthPerZone)
            self.ZoneScale = data.get('ZoneScale', self.ZoneScale)
            self.GearStatScaling = data.get('GearStatScaling', self.GearStatScaling)

        def __str__(self) -> str:
            return f"Parameters(MaxLevel={self.MaxLevel}, BaseXPPerLevel={self.BaseXPPerLevel}, XPExponent={self.XPExponent}, GoldPerCombatStep={self.GoldPerCombatStep}, GoldPerNonCombatStep={self.GoldPerNonCombatStep}, CombatChance={self.CombatChance}, DeathChance={self.DeathChance}, RepairCostPct={self.RepairCostPct}, RespecChanceCombat={self.RespecChanceCombat}, RespecBaseCost={self.RespecBaseCost}, RespecLevelMult={self.RespecLevelMult}, VendorTaxPct={self.VendorTaxPct}, ZoneTier={self.ZoneTier}, BaseXP_Combat={self.BaseXP_Combat}, BaseXP_NonCombat={self.BaseXP_NonCombat}, SkillDiff_TierMult={self.SkillDiff_TierMult}, SkillDiff_StDev={self.SkillDiff_StDev}, TimePerStep_Min={self.TimePerStep_Min}, DeathSeverity={self.DeathSeverity}, RepairCostPerZone={self.RepairCostPerZone}, StepCount={self.StepCount}, RunID={self.RunID}, Seed={self.Seed}, BaseRecommendedGear={self.BaseRecommendedGear}, GearGrowthPerZone={self.GearGrowthPerZone}, ZoneScale={self.ZoneScale}, GearStatScaling={self.GearStatScaling})"
    
    class GearQualityWeights: 
        class Tier: 
            Common: float = 0.7
            Rare: float = 0.22
            Epic: float = 0.07
            Legendary: float = 0.01

            def __init__(self, data:dict) -> None:
                self.Common = data.get('Common', self.Common)
                self.Rare = data.get('Rare', self.Rare)
                self.Epic = data.get('Epic', self.Epic)
                self.Legendary = data.get('Legendary', self.Legendary)

            def __str__(self) -> str:
                return f"Tier(Common={self.Common}, Rare={self.Rare}, Epic={self.Epic}, Legendary={self.Legendary})"
        
        class Threshold:
            Common: float = 0.4
            Rare: float = 0.7
            Epic: float = 0.9
            Legendary: float = 1

            def __init__(self, data:dict) -> None:
                self.Common = data.get('Common', self.Common)
                self.Rare = data.get('Rare', self.Rare)
                self.Epic = data.get('Epic', self.Epic)
                self.Legendary = data.get('Legendary', self.Legendary)

            def __str__(self) -> str:
                return f"Threshold(Common={self.Common}, Rare={self.Rare}, Epic={self.Epic}, Legendary={self.Legendary})"
                
        Tiers: dict[Tier] = {}
        Thresholds: dict[Threshold] = {}

        def __init__(self, data:dict) -> None:
            tiers = data.get('Tiers', None)
            for(key, value) in tiers.items():
                self.Tiers[key] = self.Tier(value)
            thresholds = data.get('Thresholds', None)
            for(key, value) in thresholds.items():
                self.Thresholds[key] = self.Threshold(value)
        
        def __str__(self) -> str:
            return f"GearQualityWeights(Tiers={self.Tiers}, Thresholds={self.Thresholds})"
    
    class DropThresholds:
        Weapon: float = 0.15
        Chest: float = 0.25
        Helm: float = 0.2
        Legs: float = 0.2
        Accessory: float = 0.2

        def __init__(self, data) -> None:
            self.Weapon = data.get('Weapon', self.Weapon)
            self.Chest = data.get('Chest', self.Chest)
            self.Helm = data.get('Helm', self.Helm)
            self.Legs = data.get('Legs', self.Legs)
            self.Accessory = data.get('Accessory', self.Accessory)

        def __str__(self) -> str:
            return f"DropThresholds(Weapon={self.Weapon}, Chest={self.Chest}, Helm={self.Helm}, Legs={self.Legs}, Accessory={self.Accessory})"
    
    class ScoreWeights:
        Common: float = 1.4
        Rare: float = 1.2
        Epic: float = 1.0
        Legendary: float = 0.9
        Zone: float = 0.6

        def __init__(self, data) -> None:
            self.Common = data.get('Common', self.Common)
            self.Rare = data.get('Rare', self.Rare)
            self.Epic = data.get('Epic', self.Epic)
            self.Legendary = data.get('Legendary', self.Legendary)
            self.Zone = data.get('Zone', self.Zone)

        def __str__(self) -> str:
            return f"ScoreWeights(Common={self.Common}, Rare={self.Rare}, Epic={self.Epic}, Legendary={self.Legendary}, Zone={self.Zone})"

    class PerQualityStat:
        AvgPower: float = 19.914285714285715
        AvgSellValue: float = 21.2
        
        def __init__(self, data) -> None:
            self.AvgPower = data.get('AvgPower', self.AvgPower)
            self.AvgSellValue = data.get('AvgSellValue', self.AvgSellValue)

        def __str__(self) -> str:
            return f"PerQualityStat(AvgPower={self.AvgPower}, AvgSellValue={self.AvgSellValue})"
    
    parameters: Parameters
    gearQualityWeights: GearQualityWeights
    dropThresholds: DropThresholds
    scoreWeights: ScoreWeights
    perQualityStats: dict[PerQualityStat] = {}

    def __init__(self, data:dict) -> None:
        self.parameters = self.Parameters(data['Parameters'])
        self.gearQualityWeights = self.GearQualityWeights(data['GearQualityWeights'])
        self.dropThresholds = self.DropThresholds(data['DropThresholds'])
        self.scoreWeights = self.ScoreWeights(data['ScoreWeights'])
        for (key, value) in data['PerQualityStats'].items():
            self.perQualityStats[key] = self.PerQualityStat(value)
    
    def __str__(self) -> str:
        return f"Inputs(parameters={self.parameters}, gearQualityWeights={self.gearQualityWeights}, dropThresholds={self.dropThresholds}, scoreWeights={self.scoreWeights}, perQualityStats={self.perQualityStats})"

class World:
    BeatNum: int
    Stage: str
    BeatName: str
    BeatStartStep: int
    ZoneLevel: int
    BeatDC: int
