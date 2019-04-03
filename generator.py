from numpy.random import choice, shuffle


class CareMember:
    def __init__(self, name, level):
        self.name = name
        self.level = level
        self.schedule = {"monday": 0, "tuesday": 0, "wednesday": 0, "thursday": 0,
                         "friday": 0, "saturday": 0, "sunday": 0}

    def increment_shift(self, day):
        self.schedule[day] += 1

    def number_of_shifts_yesterday(self, day):
        if "monday" == day:
            return self.schedule["sunday"]
        elif "tuesday" == day:
            return self.schedule["monday"]
        elif "wednesday" == day:
            return self.schedule["tuesday"]
        elif "thursday" == day:
            return self.schedule["wednesday"]
        elif "friday" == day:
            return self.schedule["thursday"]
        elif "saturday" == day:
            return self.schedule["friday"]
        elif "sunday" == day:
            return self.schedule["saturday"]

    def schedule_weight(self, day, shift_number):
        num_of_shifts = self.schedule[day]
        w = 0 if num_of_shifts >= 2 else (abs(num_of_shifts - shift_number) + 1) ** (10 + (3-self.number_of_shifts_yesterday(day)))
        # print("member: {}, shift number: {}, num of shifts: {}, num of shifts yesterday: {}, weight: {}".format(self.name, shift_number, num_of_shifts, self.number_of_shifts_yesterday(day), w))
        return w

    def __repr__(self):
        return self.name


def weights(members, day, shift_number):
    w = [member.schedule_weight(day, shift_number)for member in members]
    return w, sum(w)


def probability(members, day, shift_number):
    weights_for_day, total_weights = weights(members, day, shift_number)
    return [weight / total_weights for weight in weights_for_day]


def generate_members_for_shift(members, day, shift_number, amount):
    if day is "monday" and shift_number is 0:
        return members
    elif shift_number is 0 or shift_number is 1:
        return choice(members, p=probability(members, day, shift_number), replace=False, size=amount)
    else:
        return sorted(members, key=lambda x: x.schedule_weight(day, shift_number))[-amount:]


def schedule(members):
    for day in ["monday", "tuesday", "wednesday", "thursday", "friday"]:
        print(day)
        for shift_number in range(4):
            shuffle(members)
            members_for_shift = generate_members_for_shift(members, day, shift_number, 4)
            for member in members_for_shift:
                member.increment_shift(day)
            print(sorted(members_for_shift, key=lambda x: x.name))
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
        print("{} ({} shifts) [{}]\n{}\n".format(member.name, sum([member.schedule[day] for day in member.schedule]), member.level, member.schedule))


main()
