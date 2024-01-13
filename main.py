from data import data, champs

class champion:
    def __init__(self, id, level, points):
        self.id = id
        self.level = level
        self.points = points

masteries = []

for thing in data:
    masteries.append(champion(
        thing['championId'], 
        thing['championLevel'], 
        thing['championPoints']))

# Commented out as per instruction
# for 

# x_data = list(range(1, jumps+2))
# y_data = data_gen(simulations, jumps, probability)
# fig = plt.figure(figsize=(10, 5))

# plt.bar(x_data, data_gen(simulations, jumps, probability))

# plt.xlabel("Position")
# plt.ylabel("Probability")
# plt.suptitle("Probability distribution of the jumper landing on a given position from the left")
# plt.title("P(jumps left) = {}, Num of jumps = {}, P(jump left on 1st jump) = {}".format(probability, jumps, 0.5))
# plt.show()
