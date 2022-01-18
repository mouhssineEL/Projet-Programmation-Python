
import pygame as pg



class ResourceManager:


    def __init__(self):

        # resources
        self.resources = {
            "Wood": 10,
            "Stone": 10,
            "Gold": 10
        }

        #costs
        self.costs = {
            "House": {"Wood": 0, "Stone": 0, "Gold": 0},
            "House1": {"Wood": 7, "Stone": 3, "Gold": 1},
            "House2": {"Wood": 3, "Stone": 5, "Gold": 1},
            "barrack": {"Wood": 2, "Stone": 3, "Gold": 1}
        }

    def apply_cost_to_resource(self, building):
        for resource, cost in self.costs[building].items():
            self.resources[resource] -= cost

    def is_affordable(self, building):
        affordable = True
        for resource, cost in self.costs[building].items():
            if cost > self.resources[resource]:
                affordable = False
        return affordable

