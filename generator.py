from bitarray import bitarray
from numpy.random import choice, shuffle


NUMBER_OF_SHIFTS_PER_DAY = 4
NUMBER_OF_MEMBERS_PER_SHIFT = 4


class CareMember:
    def __init__(self, name: str, level: str):
        self.name = name
        self.level = level
        self.schedule = {"monday": bitarray(), "tuesday": bitarray(), "wednesday": bitarray(), "thursday": bitarray(),
                         "friday": bitarray(), "saturday": bitarray(), "sunday": bitarray()}

    def add_shift(self, day: str, add_to_schedule: bool):
        self.schedule[day].append(add_to_schedule)

    def number_of_shifts_yesterday(self, day: str) -> int:
        if "monday" is day:
            return self.schedule["sunday"].count()
        elif "tuesday" is day:
            return self.schedule["monday"].count()
        elif "wednesday" is day:
            return self.schedule["tuesday"].count()
        elif "thursday" is day:
            return self.schedule["wednesday"].count()
        elif "friday" is day:
            return self.schedule["thursday"].count()
        elif "saturday" is day:
            return self.schedule["friday"].count()
        elif "sunday" is day:
            return self.schedule["saturday"].count()

    def schedule_weight(self, day: str, shift_number: str) -> int:
        num_of_shifts = self.schedule[day].count()
        w = 0 if num_of_shifts >= 2 \
            else (abs(num_of_shifts - shift_number) + 1) ** (10 + (3-self.number_of_shifts_yesterday(day)))
        return w

    def __repr__(self) -> str:
        return self.name


def weights(members: [CareMember], day: str, shift_number: int) -> (int, int):
    w = [member.schedule_weight(day, shift_number)for member in members]
    return w, sum(w)


def probability(members: [CareMember], day: str, shift_number: int) -> [int]:
    weights_for_day, total_weights = weights(members, day, shift_number)
    return [weight / total_weights for weight in weights_for_day]


def generate_members_for_shift(members: [CareMember], day: str, shift_number: int, amount: int) -> [CareMember]:
    if day is "monday" and shift_number is 0:
        return members
    elif shift_number is 0 or shift_number is 1:
        return choice(members, p=probability(members, day, shift_number), replace=False, size=amount)
    else:
        return sorted(members, key=lambda x: x.schedule_weight(day, shift_number))[-amount:]


def schedule(members: [CareMember]):
    for day in ["monday", "tuesday", "wednesday", "thursday", "friday"]:
        print(day)
        for shift_number in range(NUMBER_OF_SHIFTS_PER_DAY):
            shuffle(members)
            members_for_shift = generate_members_for_shift(members, day, shift_number, NUMBER_OF_MEMBERS_PER_SHIFT)
            for member in members_for_shift:
                member.add_shift(day, True)
            for member in list(set(members) - set(members_for_shift)):
                member.add_shift(day, False)
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
        print("{} ({} shifts) [{}]\n{}\n".format(member.name,
                                                 sum([member.schedule[day].count()
                                                      for day in member.schedule]), member.level, member.schedule))


main()
