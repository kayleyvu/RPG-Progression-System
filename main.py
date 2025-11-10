import simulate
import structs
import json

if __name__ == "__main__":
    # inputs = structs.Inputs()
    # inputs.combat_chance = 100

    with open("Inputs.json", "r") as f:
        data = json.load(f)
        
    inputs = structs.Inputs(**data);

    simulate.simulate(50, inputs)
