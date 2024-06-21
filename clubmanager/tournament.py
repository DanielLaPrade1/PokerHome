import math


# Round to nearest multiple of a factor
def round_to_nearest_multiple(num, factor):
    return math.ceil(num / factor) * factor


# Calculate rounding factor based on small blind value
def calculate_rounding_factor(small_blind):
    num_digits = len(str(small_blind))
    if num_digits <= 2:
        return small_blind
    else:
        return 10 ** (num_digits - 2)


# Calculate Tournament Blind Structure
def calculate_blind_structure(num_players, starting_stack, target_duration, blind_duration, small_blind):
    total_chips = num_players * starting_stack
    num_levels = math.ceil(target_duration / blind_duration)

    original_small_blind = small_blind
    big_blind = small_blind * 2

    blind_increase_factor = (
        total_chips / (small_blind * 4)) ** (1 / num_levels)

    # Generate blind structure
    blind_structure = []
    precise_small_blind = small_blind
    for level in range(1, num_levels + 1):
        # Add current level to blind structure
        blind_structure.append(
            (level, small_blind, big_blind))

        # Next Blinds Calculation, Keep Track of 2 variables -->
        rounding_factor = calculate_rounding_factor(original_small_blind)

        # Precision variable
        precise_small_blind = round(
            precise_small_blind * blind_increase_factor)

        # Actual Small Blind (should catch up to precise small blind when necessary)
        previous_small_blind = small_blind
        small_blind = round_to_nearest_multiple(
            precise_small_blind, original_small_blind)
        if small_blind <= previous_small_blind:
            small_blind = previous_small_blind + original_small_blind
        big_blind = small_blind * 2

    return blind_structure


# Usage
# num_players = 15
# small_blind = 20
# starting_stack = 1000  # _ chips
# target_duration = 300  # _ minutes
# blind_duration = 10  # _ minutes per level

# blind_structure = calculate_blind_structure(
#     num_players, starting_stack, target_duration, blind_duration, small_blind)

# print(f"""
# Num Players {num_players}
# starting_stack = {starting_stack}
# target_duration = {target_duration}
# blind_duration = {blind_duration}
# small_blind = {small_blind}
# """)
# for level, small_blind, precise_small_blind, big_blind in blind_structure:
#     print(f"Level {level}: SB = {small_blind}, precise_SB =
#           {precise_small_blind} BB = {big_blind}")
