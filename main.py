import simulate
import structs
import json

if __name__ == "__main__":
    with open("./data/Inputs.json", "r") as f:
        data = json.load(f)
    inputs = structs.Inputs(data); # Load in inputs

    with open("./data/Worlds.json", "r") as f:
        data = json.load(f)

    worlds = []
    for(value) in data:
        worlds.append(structs.World(value)) # Load in worlds

    simulate.simulate(50, inputs, worlds)
