import random
import time  # Import time module for timing analysis and delays

def roll_dice():
    """
    Rolls three six-sided dice and returns their values as a tuple.
    
    Returns:
        tuple: A tuple containing three random integers between 1 and 6.
    """
    return (random.randint(1, 6), random.randint(1, 6), random.randint(1, 6))

def check_dice(dice):
    """
    Checks the dice roll to determine the state: if a player has 'tupled out' or has 'fixed' dice.
    
    Args:
        dice (tuple): A tuple containing the values of the three dice rolled.
        
    Returns:
        str: 'tupled_out', 'fixed', or 'none' based on the dice roll.
    """
    counts = {}
    for die in dice:
        counts[die] = counts.get(die, 0) + 1
    
    if 3 in counts.values():
        return "tupled_out"  # All dice are the same (tupled out).
    elif 2 in counts.values():
        return "fixed"  # A pair of dice are the same (fixed).
    return "none"  # No special conditions (none).

def play_turn(player_id, turn_number):
    """
    Simulates a single turn of a player in the game. The player rolls dice, checks for conditions,
    and decides whether to reroll or stop.
    
    Args:
        player_id (int): The ID of the player (1-based).
        turn_number (int): The current turn number.
        
    Returns:
        int: The score the player earns for the turn.
    """
    start_time = time.time()  # Record the start time of the turn
    
    print(f"\nPlayer {player_id}'s turn {turn_number}:")
    dice = roll_dice()
    print(f"Initial roll: {dice}")
    
    dice_state = check_dice(dice)
    fixed_dice = []
    
    if dice_state == "tupled_out":
        print("Tupled out! No points for this round.")
        end_time = time.time()  # Record the end time of the turn
        print(f"Turn duration: {end_time - start_time:.2f} seconds.")
        return 0
    
    while True:
        reroll_choice = input("Do you want to reroll? (yes/no): ").strip().lower()
        
        if reroll_choice == 'no':
            score = sum(dice)
            print(f"Player {player_id} stops with {score} points this round.")
            end_time = time.time()  # Record the end time of the turn
            print(f"Turn duration: {end_time - start_time:.2f} seconds.")
            return score
        
        # Reroll the dice that are not fixed
        if dice_state == "fixed":
            fixed_dice = [die for die in dice if dice.count(die) == 2]
            dice = tuple(random.randint(1, 6) if die not in fixed_dice else die for die in dice)
        else:
            dice = roll_dice()
        
        print(f"New roll: {dice}")
        dice_state = check_dice(dice)
        
        if dice_state == "tupled_out":
            print("Tupled out! No points for this round.")
            end_time = time.time()  # Record the end time of the turn
            print(f"Turn duration: {end_time - start_time:.2f} seconds.")
            return 0
        elif dice_state == "fixed":
            fixed_dice = [die for die in dice if dice.count(die) == 2]
            print(f"Fixed dice: {fixed_dice}")

def start_game():
    """
    Starts the dice game, managing the number of players, their turns, and the scoring.
    
    Prompts the user for the number of players and handles the game logic for each turn.
    """
    try:
        num_players = int(input("Enter number of players: ").strip())
        if num_players < 1:
            raise ValueError("Number of players must be greater than zero.")
    except ValueError as e:
        print(f"Invalid input. Please enter a valid number of players. ({e})")
        return
    
    # Create a list of players
    players = [{"id": i + 1, "score": 0} for i in range(num_players)]

    max_turns = 5  # Fixed number of turns
    
    game_start_time = time.time()  # Track the start time of the entire game
    
    for turn in range(1, max_turns + 1):
        print(f"\n--- Turn {turn} ---")
        
        for player in players:
            turn_score = play_turn(player["id"], turn)
            player["score"] += turn_score
            print(f"Player {player['id']}'s total score after turn {turn}: {player['score']}")
            time.sleep(1)  # Adding a delay between players for pacing

    game_end_time = time.time()  # Track the end time of the entire game
    total_game_duration = game_end_time - game_start_time
    print(f"\nTotal game duration: {total_game_duration:.2f} seconds.")
    
    # Determine and print the winner
    winner = max(players, key=lambda p: p["score"])
    print(f"\nPlayer {winner['id']} wins with {winner['score']} points!")

    # Write the results to a file
    with open("game_results.txt", "w") as file:
        for player in players:
            file.write(f"Player {player['id']}: {player['score']} points\n")
    print("\nGame results have been saved to 'game_results.txt'.")

# Start the game
start_game()
