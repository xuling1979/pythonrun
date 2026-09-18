with open("mods") as f:
    all=f.read().splitlines()
for mod in all:
    print("import",mod)