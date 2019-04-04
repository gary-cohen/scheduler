from bitarray import bitarray
from numpy.random import choice, shuffle
from random import randint

import math
import numpy as np

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
        if "monday" == day:
            return self.schedule["sunday"].count()
        elif "tuesday" == day:
            return self.schedule["monday"].count()
        elif "wednesday" == day:
            return self.schedule["tuesday"].count()
        elif "thursday" == day:
            return self.schedule["wednesday"].count()
        elif "friday" == day:
            return self.schedule["thursday"].count()
        elif "saturday" == day:
            return self.schedule["friday"].count()
        elif "sunday" == day:
            return self.schedule["saturday"].count()

    def schedule_weight(self, day: str, shift_number: str) -> int:
        num_of_shifts = self.schedule[day].count()
        w = (abs(num_of_shifts - shift_number) + 1) ** (10 + (3-self.number_of_shifts_yesterday(day)))
        return w

    def __repr__(self) -> str:
        return self.name


def weights(members: [CareMember], day: str, shift_number: int) -> (int, int):
    w = [member.schedule_weight(day, shift_number) for member in members]
    return w, sum(w)


def probability(members: [CareMember], day: str, shift_number: int) -> [int]:
    weights_for_day, total_weights = weights(members, day, shift_number)
    return [weight / total_weights for weight in weights_for_day]


def get_members_by_level(members: [CareMember]) -> ([CareMember], [CareMember]):
    experienced_members = []
    new_members = []

    for member in members:
        if "experienced" == member.level:
            experienced_members.append(member)
        else:
            new_members.append(member)

    return experienced_members, new_members


def get_amount_of_members(experienced_members: [CareMember], new_members: [CareMember], total: int) -> (int, int):
    # we need at least one experienced member per shift
    max_number_of_experienced = math.floor((len(experienced_members) / len(new_members)) * total) \
        if len(new_members) > 0 else 1
    number_of_experienced = 1 if max_number_of_experienced == 1 else randint(1, max_number_of_experienced)
    return number_of_experienced, total - number_of_experienced


def get_members_for_shift(members: [CareMember], day: str, shift_number: int, total: int) -> [CareMember]:
    if "monday" == day and shift_number == 0:
        return members
    elif shift_number == 0 or shift_number == 1:
        experienced_members, new_members = get_members_by_level(members)
        amount_of_experienced_members, amount_of_new_members = get_amount_of_members(experienced_members, new_members, total)
        experienced_choice = choice(experienced_members,
                                    p=probability(experienced_members, day, shift_number),
                                    replace=False,
                                    size=amount_of_experienced_members).tolist()
        new_choice = choice(new_members,
                            p=probability(new_members, day, shift_number),
                            replace=False,
                            size=amount_of_new_members).tolist()
        return experienced_choice + new_choice
    else:
        non_available_members = []

        # if a member was scheduled for shift 1, they cannot be scheduled in shift 2
        if shift_number == 2:
            for member in members:
                if member.schedule[day][1]:
                    non_available_members.append(member)

        # if a member has at least two shifts they're done for the day
        if shift_number >= 2:
            for member in members:
                if member.schedule[day].count() == 2:
                    non_available_members.append(member)

        available_members = list(set(members) - set(non_available_members))

        experienced_members, new_members = get_members_by_level(available_members)
        amount_of_experienced_members, amount_of_new_members = get_amount_of_members(experienced_members, new_members, total)
        experienced_choice = sorted(experienced_members, key=lambda x: x.schedule_weight(day, shift_number))[-amount_of_experienced_members:]
        new_choice = sorted(new_members, key=lambda x: x.schedule_weight(day, shift_number))[-amount_of_new_members:]
        return experienced_choice + new_choice


def schedule(members: [CareMember]):
    for day in ["monday", "tuesday", "wednesday", "thursday", "friday"]:
        print(day)
        for shift_number in range(NUMBER_OF_SHIFTS_PER_DAY):
            shuffle(members)
            members_for_shift = get_members_for_shift(members, day, shift_number, NUMBER_OF_MEMBERS_PER_SHIFT)
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
