import json
fencer1 = ""
fencer1score = 0
fencer1location = 0
fencer1rating = 0
fencer1finalrating = 0

fencer2 = ""
fencer2score = 0
fencer2location = 0
fencer2rating = 0
fencer2finalrating = 0

winner = ""

with open("./fencingmatches.json", "r") as file:
    matches = json.load(file)

with open("./fencers.json", "r") as file:
    fencers = json.load(file)

for match in matches:
    winner = match["Winning Fencer"]
    for i, fencer in enumerate(fencers):
        if match["Fencer 1"] == fencer["name"]:
            fencer1 = fencer["name"]
            fencer1score = match["Fencer 1 Score"]
            fencer1location = i 
            fencer1rating = fencer["rating"]
        elif match["Fencer 2"] == fencer["name"]:
            fencer2 = fencer["name"]
            fencer2score = match["Fencer 2 Score"]
            fencer2location = i
            fencer2rating = fencer["rating"]




    fencer1p = fencer1rating / (fencer1rating + fencer2rating)
    fencer2p = fencer2rating / (fencer1rating + fencer2rating)

    
    if winner == fencer1:
        k = 30 + (fencer1score - fencer2score)
        fencer1rating = fencer1rating + k*(1-fencer1p) + 0.01
        fencer2rating = fencer2rating + k*(0-fencer2p) + 0.01
    elif winner == fencer2:
        k = 30 + (fencer2score - fencer1score)*1.1
        fencer1rating = fencer1rating + k*(0-fencer1p) + 0.01
        fencer2rating = fencer2rating + k*(1-fencer2p) + 0.01
    fencer1rating = round(fencer1rating)
    fencer2rating = round(fencer2rating)

    fencers[fencer1location].update(rating=fencer1rating)
    fencers[fencer2location].update(rating=fencer2rating)
    
    with open("./fencers.json", "w") as file:
        json.dump(fencers, file, indent = 4)



