import json

f = open("dataBase.json", "r")
jsonData = json.load(f)
thrust = jsonData["thrustMenu"]
a = []
print(thrust.values())
for i in (thrust.values()):
    a.append(i)

print(a)