from typing import Dict, List, Tuple
from util import Color, Sat, User, Vector3
import math
import random

MAX_BEAM_ANGLE = 45
MAX_USERS = 32
MIN_INF_BEAM_ANGLE = 10
MAX_COLORS = 4

random.seed()

def color_next(color):
    color = color + 1
    if color > MAX_COLORS:
        color = 1
    return color

def sum_rows(viable_cxns, rows, cols):
    row_sums = []
    for r in range(rows):
        sum = 0
        for c in range(cols):
            if viable_cxns[r][c] >= 1:
                sum += 1
        row_sums.append(sum)
    return row_sums

def sum_cols(viable_cxns, rows, cols):
    col_sums = []
    for c in range(cols):
        sum = 0
        for r in range(rows):
            if viable_cxns[r][c] >= 1:
                sum += 1
        col_sums.append(sum)
    return col_sums


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# SORT NORMALIZED USERS and SATS by DOT PRODUCT with BASIS VECTOR
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def sort_values(values, n_values, index_shift):
    values_sorted = []
    
    # Normalize values with a scaling function
    x_big = y_big = z_big = 1
    for i in range(n_values):

        # Find largest x, y, and z values
        x = abs(values[i + index_shift].x)
        y = abs(values[i + index_shift].y)
        z = abs(values[i + index_shift].z)
        if x > x_big: x_big = x
        if y > y_big: y_big = y
        if z > z_big: z_big = z

    scale_V = Vector3(x_big, y_big, z_big)
    #print("x big:", x_big, "y big:", y_big, "z big:", z_big)

    # Get dot product of normalized vector with basis vector, store in list
    basis_vector = Vector3(1,1,1)
    for i in range(n_values):
        # FOUND BUG HERE... ALTERING A REFERENCE TO USER OR SAT INSTAD OF MAKING A COPY
        value = Vector3(values[i + index_shift].x, values[i + index_shift].y, values[i + index_shift].z) 
        value_unit = value.unit()
        
        value.x = value.x / scale_V.x
        value.y = value.y / scale_V.y
        value.z = value.z / scale_V.z
        #print("vector scaled", value)
        
        dot_prod = value.dot(basis_vector)  # SCALED DOT_PROD
        dot_prod_unit = value_unit.dot(basis_vector)    # UNIT DOT_PROD INSTEAD
        vlue_dot = (i + index_shift, dot_prod) 
        values_sorted.append(vlue_dot)

    # Sort lists by second value (dot product) in tuple in descending order
    values_sorted.sort(key=lambda a: a[1], reverse=True)

    return values_sorted

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# VIABLE CONNECTION GEOMETRY for LOCAL BEAM INTERFERENCE and FREQUENY
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def check_beam_interferance(sats, users, viable_cxns, sats_sorted, users_sorted, index_shift_sats, index_shift_users, generous):
    for s_tuple in sats_sorted:
        index_s = s_tuple[0] - index_shift_sats
        s_V = sats[s_tuple[0]]

        # Build list of all viable users for the sat
        viable_users = []
        for u_tuple in users_sorted:
            index_u = u_tuple[0] - index_shift_users
            # Viable beam
            if viable_cxns[index_s][index_u] >= 1:
                viable_users.append((u_tuple[0], u_tuple[1]))    # Tuple (user id, dot product)
        #print(viable_users)

        # Check pairwise viable_users against viable_users for interferance angle
        # Trying to distribute users evenly while removing some
        for i,u1_tuple in enumerate(viable_users):
            index_u1 = u1_tuple[0] - index_shift_users
            u1_V = users[u1_tuple[0]]

            j = i + 1   # Don't repeat beams pairs already examined
            while j < len(viable_users):
                index_u2 = viable_users[j][0] - index_shift_users
                u2_V = users[viable_users[j][0]]

                """ Calc beam angle between each satellite and two users """
                user_interf_angle = s_V.angle_between(u1_V, u2_V)
                #print("User Interference Angle:", user_interf_angle)

                # Angle is larger than interferance angle
                if user_interf_angle < MIN_INF_BEAM_ANGLE:
                    color_u1 = viable_cxns[index_s][index_u1]
                    color_u2 = viable_cxns[index_s][index_u2]
                    #print("\nu1:", u1_tuple[0], "-- dot_prod:", u1_tuple[1], "-- color_u1:", viable_cxns[index_s][index_u1])
                    #print("u2:", viable_users[j][0], "-- dot_prod:", viable_users[j][1],"-- color_u2:", viable_cxns[index_s][index_u2])

                    # Check beam color 
                    if color_u1 == color_u2:
                        # DESIGN DECISION: rotate colors if generous, otherwise delete it
                        if generous:
                            color = color_next(color_u2)
                            viable_cxns[index_s][index_u2] = color
                        else:
                            viable_cxns[index_s][index_u2] = 0
                    
                # Increment j index so don't revisit previous user pairs
                j += 1


def solve(users: Dict[User, Vector3], sats: Dict[Sat, Vector3]) -> Dict[User, Tuple[Sat, Color]]:
    """Assign users to satellites respecting all constraints."""
    solution = {}

    # Get index shift for satellite and users data. Id indexing may start at 0 or 1 
    index_shift_sats = int(list(sats.keys())[0])    # Value added to 0 to get first sat
    index_shift_users = int(list(users.keys())[0])  # Value added to 0 to get first user

    # Get number of users and satellites
    n_users = len(users)
    n_sats = len(sats)

    # Sort normalize users and sats using a scaling function
    users_sorted = sort_values(users, n_users, index_shift_users)
    sats_sorted = sort_values(sats, n_sats, index_shift_sats)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # VIABLE CONNECTIONS given BEAM ANGLE
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # THE BUG WAS HERE! IMPROPERLY INITIALIZING THE ARRAY, ALL ROWS POINTING TO SAME ROW
    #viable_cxns = [[0] * n_users] * n_sats  
    viable_cxns = []
    for s in range(n_sats):
        viable_cxns.append([0] * n_users)

    # Initialize color to 'A'
    color = 1

    for u_tuple in users_sorted:
        user = users[u_tuple[0]]

        for s_tuple in sats_sorted:
            sat = sats[s_tuple[0]]

            center = Vector3(0,0,0)
            beam_angle = 180 - user.angle_between(center, sat)
            #print("beam angle", beam_angle)

            # Check beam angle GOOD
            if beam_angle < MAX_BEAM_ANGLE:
                index_s = s_tuple[0] - index_shift_sats
                index_u = u_tuple[0] - index_shift_users
                viable_cxns[index_s][index_u] = color_next(color)

    """
    # TESTING - column totals (sats per user)
    col_tots = sum_cols(viable_cxns, n_sats, n_users)
    print("col_tots:", col_tots)

    row_tots = sum_rows(viable_cxns, n_sats, n_users)
    print("row_tots:", row_tots)
    """
    
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # PRUNE EXTRA SATS RANDOMLY per USER
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # First get total number of sats per user
    col_totals = sum_cols(viable_cxns, n_sats, n_users)
    #print("col_totals", col_totals)

    # If a user has more than 1 satellite, remove sats after the first one
    for u in range(n_users):
        user_sats = col_totals[u]

        # User has more than 1 viable satellite
        if user_sats > 1:
            # Build list of all viable sats for the user
            viable_sats = []
            for s_tuple in sats_sorted:
                index_s = s_tuple[0] - index_shift_sats
                # Viable beam
                if viable_cxns[index_s][u] >= 1:
                    viable_sats.append((s_tuple[0], s_tuple[1]))    # Tuple (sat id, dot product)

            # Shuffle viable_sats and choose first sat. Save color value
            viable_sats = sorted(viable_sats, key=lambda x: random.random())
            index_chosen = viable_sats[0][0] - index_shift_sats
            color = viable_cxns[index_chosen][u]

            # Remove all cxns 
            for s_tuple in viable_sats:
                index_s = s_tuple[0] - index_shift_sats
                viable_cxns[index_s][u] = 0

            # Add back chosen cxn
            viable_cxns[index_chosen][u] = color

            
    # Check beams from each satellite for interference on SORTED LIST OF SATS
    iterations = 2
    generous = True # Rotate color 
    for i in range(iterations):
        check_beam_interferance(sats, users, viable_cxns, sats_sorted, users_sorted, index_shift_sats, index_shift_users, generous)
    
    generous = False   # Remove connection
    check_beam_interferance(sats, users, viable_cxns, sats_sorted, users_sorted, index_shift_sats, index_shift_users, generous)


    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # PRUNE EXTRA USERS per SATELLITE
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # First get total number of users per sat
    row_totals = sum_rows(viable_cxns, n_sats, n_users)
    #print("row_totals", row_totals)

    # If a sat has more than 1 user, remove users after the first one
    for s in range(n_sats):
        sat_users = row_totals[s]

        # Sat has more than 1 viable user
        if sat_users > MAX_USERS:
            users_allocated = 0

            # Searching users for viable connections
            for u in range(n_users):

                # Found a viable cxn
                if viable_cxns[s][u] >= 1:

                    # Keep first sat cxn found
                    if users_allocated < MAX_USERS:
                        users_allocated += 1
                    
                    # Already have max users allocated
                    else:
                        # Remove connection
                        viable_cxns[s][u] = 0


    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # FORMAT SOLUTION
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    for u in range(n_users):
        for s in range(n_sats):
            if viable_cxns[s][u] >= 1:
                color = viable_cxns[s][u]
                solution[u + index_shift_users] = (s + index_shift_sats, color)
    
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print('Sats: ', n_sats, ' Users: ', n_users)
    coverage = sum(sum_rows(viable_cxns, n_sats, n_users)) / n_users
    print("Coverage:", coverage)
    print()

    return solution