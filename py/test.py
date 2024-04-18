#!/usr/bin/env python3

import collections
import datetime
import math
import os
import sys

from solution import solve
from test_util import BOLD, GRAY, GREEN, RED, RESET, YELLOW, check, fail
from util import Color, Vector3

TIMEOUT = datetime.timedelta(seconds=600)


class Scenario(object):

    def __init__(self, path: str):
        super().__init__()

        self.sats = {}
        self.users = {}
        self.min_coverage = 1.0

        for line in open(path):
            line = line.split('#')[0].strip()
            if line == '':
                continue

            parts = line.split()
            if parts[0] == 'min_coverage':
                self.min_coverage = float(parts[1])
            elif parts[0] == 'sat':
                self.sats[int(parts[1])] = Vector3(
                    float(parts[2]), float(parts[3]), float(parts[4]))
            elif parts[0] == 'user':
                self.users[int(parts[1])] = Vector3(
                    float(parts[2]), float(parts[3]), float(parts[4]))
            else:
                fail("Invalid token: %r" % parts[0])

    def check(self, solution):
        beams = collections.defaultdict(list)

        for user, (sat, color) in solution.items():
            user_pos = self.users[user]
            sat_pos = self.sats[sat]
            check(color in Color, 'Invalid color: %r' % color)

            angle = math.degrees(math.acos(user_pos.unit().dot((sat_pos - user_pos).unit())))
            check(
                angle <= 45,
                "User %d cannot see satellite %d (%.2f degrees from vertical)" % (user, sat, angle))

            beams[sat].append((color, user))

        for sat, sat_beams in beams.items():
            sat_pos = self.sats[sat]
            check(
                len(sat_beams) <= 32, "Satellite %d cannot serve more than 32 users (%d assigned)" %
                (sat, len(sat_beams)))
            for color1, user1 in sat_beams:
                for color2, user2 in sat_beams:
                    if color1 == color2 and user1 != user2:
                        user1_pos = self.users[user1]
                        user2_pos = self.users[user2]
                        angle = sat_pos.angle_between(user1_pos, user2_pos)
                        check(
                            angle >= 10.0,
                            "Users %d and %d on satellite %d %s are too close (%.2f degrees)" %
                            (user1, user2, sat, color1, angle))

        coverage = 1.0 * len(solution) / len(self.users)
        check(coverage >= self.min_coverage, "Too few users served")


def main():
    if len(sys.argv) != 3:
        print("USAGE: %s OUT_PATH TEST_CASE" % sys.argv[0])
        sys.exit(1)

    out_path = sys.argv[1]
    test_case = sys.argv[2]

    scenario = Scenario(test_case)

    print((GRAY + "Scenario: " + RESET + "%.2f%% coverage (%d users, %d sats)" + RESET) % (
        100 * scenario.min_coverage,
        len(scenario.users),
        len(scenario.sats),
    ))

    start = datetime.datetime.now()
    solution = solve(scenario.users, scenario.sats)
    duration = datetime.datetime.now() - start
    covered = 1.0 * len(solution) / len(scenario.users)

    print((GRAY + "Solution: " + RESET + BOLD + "%s%.2f%%" + RESET + " coverage (%d users) in %s" +
           BOLD + "%.2fs" + RESET) % (
               GREEN if covered >= scenario.min_coverage else RED,
               100.0 * len(solution) / len(scenario.users),
               len(solution),
               RED if duration > TIMEOUT else YELLOW if duration > TIMEOUT / 2 else GREEN,
               duration.total_seconds(),
           ))

    with open(out_path, 'a') as out:
        out.write('%-44s %6.2f%% %6.2fs\n' % (test_case, 100.0 * covered, duration.total_seconds()))

    check(duration < TIMEOUT, "Took too long to produce a solution")
    scenario.check(solution)


if __name__ == '__main__':
    main()
