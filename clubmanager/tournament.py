import math


# Round to nearest multiple of a factor
def round_to_nearest_multiple(num, factor):
    return math.ceil(num / factor) * factor


# Calculate rounding factor based on small blind value
# Need to prioritize 2x, 5x and 10x small blind
def calculate_rounding_factor(small_blind, original_small_blind):
    if (small_blind // 250) > original_small_blind:
        return original_small_blind * 100
    elif (small_blind // 25) > original_small_blind:
        return original_small_blind * 10
    elif (small_blind // 13) > original_small_blind:
        return original_small_blind * 5
    elif (small_blind // 5) > original_small_blind:
        return original_small_blind * 2
    return original_small_blind


# Format Time
def format_time(minutes):
    hours = 0
    time = f'{hours:02d}:{minutes:02d}'
    if minutes >= 60:
        hours = minutes // 60
        minutes = minutes % 60
        time = f'{hours:02d}:{minutes:02d}'
    return time


# Calculate Tournament Blind Structure
def calculate_blind_structure(num_players, starting_stack, target_duration, blind_duration, small_blind):
    original_small_blind = small_blind
    total_chips = num_players * starting_stack
    num_levels = round(target_duration / blind_duration)

    big_blind = small_blind * 2

    # Blind Increase Multiple
    #   Used for calculating current small blind from previous small blind
    final_bb = total_chips * 0.05
    blind_increase_factor = (
        (final_bb / big_blind) ** (1 / num_levels))

    # Generate blind structure
    blind_structure = []
    precise_small_blind = small_blind
    for level in range(1, num_levels + 1):
        # Add current level to blind structure
        blind_structure.append(
            (level, small_blind, big_blind, format_time(blind_duration * level)))

        # Next Blinds Calculation, Keep Track of 2 variables -->
        # 1. Precision variable
        precise_small_blind = math.ceil(
            precise_small_blind * blind_increase_factor)

        # Small blind rounding
        rounding_factor = calculate_rounding_factor(
            small_blind, original_small_blind)

        # 2. Actual Small Blind (should hang around precise small blind with rounding applied)
        small_blind = round_to_nearest_multiple(
            precise_small_blind, rounding_factor)
        big_blind = small_blind * 2

    return blind_structure


# Usage
# num_players = 20
# small_blind = 1
# starting_stack = 200  # _ chips
# target_duration = 240  # _ minutes
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
# for level, small_blind, big_blind, time in blind_structure:
#     print(f"Level {level}: SB = {small_blind}, BB = {big_blind}, Time: {time}")
