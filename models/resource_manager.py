import pygame


class ResourceManager():
    def __init__(self):
        self.resources = {
            "food": 900,
            "wood": 900,
            "stone": 900,
            "gold": 900
        }

        self.costs = {
            "House": {"wood": 25},
            "Towncenter": {"wood": 200},
            "Barracks": {"wood": 125},
            "castel": {"wood": 150},
            "Stable": {"wood": 150},
            "SmallWall": {"food": 50, "stone": 50},
            "SmallWall1": {"food": 50, "stone": 50},
            "SmallWall2": {"food": 50, "stone": 50},
            "Archer": {"food": 40, "wood": 20},
            "AxeThrower": {"food": 50},
            "Scout": {"food": 70, "gold": 80},
            "Villager": {"food": 50},
            "ScoutShip": {"food": 20},
            "Clubman": {"food": 50},
            "upgrade": {"food": 100, "stone": 100, "wood": 100}

        }
        self.ages = {
            "House": 0,
            "Towncenter": 0,
            "Barracks": 0,
            "castel": 1,
            "Stable": 1,
            "SmallWall": 1,
            "SmallWall1": 1,
            "SmallWall2": 1,
            "Archer": 1,
            "Axemen": 1,
            "Scout": 1,
            "Villageois": 0,
            "ScoutShip": 1,
            "Clubman": 0,
            "upgrade": 0

        }

    def apply_cost_to_resource(self, building):
        for resource, cost in self.costs[building].items():
            self.resources[resource] -= cost

    def is_affordable(self, building):
        affordable = True


        return affordable

    def whatage(self, building):
        age = self.ages[building]
        return age