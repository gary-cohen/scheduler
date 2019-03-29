from numpy.random import choice


class CareMember:
    def __init__(self, name, level):
        self.name = name
        self.level = level
        self.schedule = {"monday": 0, "tuesday": 0, "wednesday": 0, "thursday": 0,
                         "friday": 0, "saturday": 0, "sunday": 0}

    def increment_shift(self, day):
        self.schedule[day] += 1

    def __repr__(self):
        return self.name


def weights(members, day, iteration):
    shifts = [member.schedule[day] for member in members]
    w = [0 if num_of_shifts >= 2 else abs(num_of_shifts - iteration) + 1 for num_of_shifts in shifts]
    return w, sum(w)


def probability(members, day, iteration):
    weights_for_day, total_weights = weights(members, day, iteration)
    return [weight / total_weights for weight in weights_for_day]


def schedule(members):
    for day in ["monday", "tuesday", "wednesday", "thursday", "friday"]:
        print(day)
        for i in range(4):
            shift = choice(members, p=probability(members, day, i), replace=False, size=4)
            for member in shift:
                member.increment_shift(day)
            print(sorted(shift, key=lambda x: x.name))
        print("")


def main():
    members = [CareMember("leo", "experienced"),
               CareMember("melanie", "new"),
               CareMember("chloe", "new"),
               CareMember("celine", "experienced"),
               CareMember("francois", "experienced"),
               CareMember("manon", "new"),
               CareMember("naim", "new"),
               CareMember("benjamin", "new"),
               CareMember("caroline", "experienced"),
               CareMember("alice", "new"),
               CareMember("berangere", "new"),
               CareMember("anna", "experienced")]

    schedule(members)
    for member in members:
        print("{} ({} shifts)\n{}\n".format(member.name, sum([member.schedule[day] for day in member.schedule]), member.schedule))


main()
