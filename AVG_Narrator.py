import sys
import random

game_state = {
    "current_location": "dark_cave",
    "inventory": [],
    "game_flags": {
        "door_unlocked": False,
        "monster_defeated": False
    }
}

location_data = {
    "dark_cave": {
        "description": "You are in a dimly lit cave. To the north, you see a faint light. There is a rusty sword lying on the damp ground.",
        "exits": {"north": "forest_path"},
        "items": ["rusty_sword"],
        "conditions": {}
    },
    "forest_path": {
        "description": "You emerge from the cave into a sunlit forest. A winding path leads east. To the south, you can see the cave entrance. Near a gnarled tree root, you spot a small, old key.",
        "exits": {"south": "dark_cave", "east": "old_shack"},
        "items": ["old_key"],
        "conditions": {}
    },
    "old_shack": {
        "description": "You stand before an old, dilapidated shack. The wooden door looks sturdy and is clearly locked. There's a faint smell of dust and old wood.",
        "exits": {"west": "forest_path"},
        "items": [],
        "conditions": {"door_locked": True}
    },
    "inside_shack": {
        "description": "You are inside the dusty, old shack. The air is still. In the corner, you see a menacing-looking goblin! It glares at you.",
        "exits": {"west": "forest_path"},
        "items": [],
        "conditions": {"monster_present": True}
    },
    "shack_cleared": {
        "description": "You are inside the dusty, old shack. The goblin lies motionless on the floor. Now that it's clear, you notice a shiny gold coin on the table.",
        "exits": {"west": "forest_path"},
        "items": ["gold_coin"],
        "conditions": {"monster_present": False}
    }
}

item_data = {
    "rusty_sword": {
        "description": "A well-used, but very rusty sword. It feels heavy in your hand.",
        "action_description": "You swing the rusty sword with a satisfying swish, but it hits nothing.",
        "takeable": True
    },
    "old_key": {
        "description": "A small, ornate, brass key. It looks like it might unlock an old wooden door.",
        "unlocks": "old_shack_door",
        "takeable": True
    },
    "gold_coin": {
        "description": "A shiny gold coin. It sparkles in the dim light.",
        "action_description": "You admire the gold coin. It's quite pretty.",
        "takeable": True
    }
}

GO_KEYWORDS = ["go", "move", "walk", "run", "enter"]
LOOK_KEYWORDS = ["look", "examine", "inspect", "observe"]
TAKE_KEYWORDS = ["take", "get", "pick up", "grab"]
USE_KEYWORDS = ["use", "apply"]
INVENTORY_KEYWORDS = ["inventory", "i", "items", "bag"]


def display_current_location():

    loc_key = game_state["current_location"]

    if loc_key == "inside_shack" and game_state["game_flags"]["monster_defeated"]:
        loc_key = "shack_cleared"

    current_loc = location_data[loc_key]
    print("\n--- Current Location ---")
    print(current_loc["description"])

    if current_loc["conditions"].get("monster_present") and not game_state["game_flags"]["monster_defeated"]:
        print("The goblin is hostile! You must fight to proceed.")
    else:
        items = current_loc.get("items", [])
        if items:
            print(f"You see: {', '.join(i.replace('_', ' ') for i in items)}.")

    print("------------------------")


def parse_input(user_input):
    words = user_input.lower().split()
    if not words:
        return {"verb": "unknown"}

    verb = words[0]
    cmd = {"verb": verb}
    stop_words = ["the", "a", "an", "at", "in", "to"]
    clean_words = [w for w in words if w not in stop_words]

    if any(k in GO_KEYWORDS for k in clean_words):
        cmd["verb"] = "go"
        for w in clean_words:
            if w in ["north", "south", "east", "west", "up", "down", "enter"]:
                cmd["direction"] = w
                break
    elif any(k in LOOK_KEYWORDS for k in clean_words):
        cmd["verb"] = "look"
        cmd["target"] = "_".join(clean_words[1:]) if len(clean_words) > 1 else "around"
    elif any(k in TAKE_KEYWORDS for k in clean_words):
        cmd["verb"] = "take"
        cmd["item"] = "_".join(clean_words[1:]) if len(clean_words) > 1 else None
    elif any(k in USE_KEYWORDS for k in clean_words):
        cmd["verb"] = "use"
        if len(clean_words) > 1:
            try:
                split_word = "on" if "on" in clean_words else "with"
                i = clean_words.index(split_word)
                cmd["item"] = "_".join(clean_words[1:i])
                cmd["target"] = "_".join(clean_words[i + 1:])
            except ValueError:
                cmd["item"] = "_".join(clean_words[1:])
                cmd["target"] = None
    elif any(k in INVENTORY_KEYWORDS for k in clean_words):
        cmd["verb"] = "inventory"
    elif verb == "fight" or ("fight" in clean_words and "goblin" in clean_words):
        cmd["verb"] = "fight"
        cmd["target"] = "goblin"

    return cmd


def combat_encounter(monster):
    print(f"\n--- Combat with the {monster.replace('_', ' ')}! ---")

    if "rusty_sword" not in game_state["inventory"]:
        print(f"You face the {monster.replace('_', ' ')} with your bare hands. It does not end well.")
        print("\n--- GAME OVER ---")
        sys.exit()

    print("You grip your rusty sword. You must roll a 5 or higher (out of 10) to win.")
    input("Press Enter to roll the die...")

    roll = random.randint(1, 10)
    print(f"You rolled a {roll}!")

    if roll >= 5:
        print(f"Success! You valiantly defeat the {monster.replace('_', ' ')}!")
        game_state["game_flags"]["monster_defeated"] = True
        game_state["current_location"] = "shack_cleared"
        display_current_location()
    else:
        print("Your attack is clumsy. The goblin dodges and lands a fatal blow.")
        print("\n--- GAME OVER ---")
        sys.exit()


def handle_go_command(cmd):
    direction = cmd.get("direction")
    if not direction:
        print("Go where?")
        return

    loc_key = game_state["current_location"]
    if loc_key == "inside_shack" and game_state["game_flags"]["monster_defeated"]:
        loc_key = "shack_cleared"

    exits = location_data[loc_key]["exits"]
    if direction in exits:
        next_loc = exits[direction]
        if next_loc == "inside_shack":
            if location_data["old_shack"]["conditions"].get("door_locked"):
                print("The door to the shack is locked. You need a key.")
                return
            if not game_state["game_flags"]["monster_defeated"]:
                print("A menacing goblin blocks your way!")
                game_state["current_location"] = "inside_shack"

        game_state["current_location"] = next_loc
        print(f"You go {direction}.")
        display_current_location()
    else:
        print(f"You can't go {direction} from here.")


def handle_look_command(cmd):
    target = cmd.get("target")
    loc_key = game_state["current_location"]
    if loc_key == "inside_shack" and game_state["game_flags"]["monster_defeated"]:
        loc_key = "shack_cleared"

    if target == "around":
        display_current_location()
    elif target in location_data[loc_key]["items"] or target in game_state["inventory"]:
        print(item_data.get(target, {}).get("description", f"It's a {target.replace('_', ' ')}."))
    else:
        print(f"You don't see a {target.replace('_', ' ')} here.")


def handle_take_command(cmd):
    item_to_take = cmd.get("item")
    if not item_to_take:
        print("Take what?")
        return

    loc_key = game_state["current_location"]
    if loc_key == "inside_shack" and game_state["game_flags"]["monster_defeated"]:
        loc_key = "shack_cleared"

    if item_to_take in location_data[loc_key]["items"]:
        if item_data.get(item_to_take, {}).get("takeable"):
            game_state["inventory"].append(item_to_take)
            location_data[loc_key]["items"].remove(item_to_take)
            print(f"You pick up the {item_to_take.replace('_', ' ')}.")
            if item_to_take == "gold_coin":
                print("\n--- CONGRATULATIONS! ---")
                print("You've found the treasure and completed your adventure!")
                sys.exit()
        else:
            print(f"You can't take the {item_to_take.replace('_', ' ')}.")
    else:
        print(f"You don't see a {item_to_take.replace('_', ' ')} here.")


def handle_use_command(cmd):
    item_to_use = cmd.get("item")
    target = cmd.get("target")
    if not item_to_use:
        print("Use what?")
        return

    if item_to_use not in game_state["inventory"]:
        print(f"You don't have a {item_to_use.replace('_', ' ')}.")
        return

    if item_to_use == "old_key" and target in ["door", "old_shack_door"] and game_state[
        "current_location"] == "old_shack":
        if location_data["old_shack"]["conditions"].get("door_locked"):
            location_data["old_shack"]["conditions"]["door_locked"] = False
            game_state["game_flags"]["door_unlocked"] = True
            location_data["old_shack"]["exits"]["enter"] = "inside_shack"
            location_data["old_shack"]["exits"]["east"] = "inside_shack"
            print("The door clicks open. You can now 'enter' the shack or 'go east' into it.")
        else:
            print("The door is already unlocked.")
        return

    if item_to_use == "rusty_sword" and target == "goblin" and game_state["current_location"] == "inside_shack":
        if not game_state["game_flags"]["monster_defeated"]:
            combat_encounter("goblin")
        else:
            print("The goblin is already defeated.")
        return

    if item_data.get(item_to_use, {}).get("action_description"):
        print(item_data[item_to_use]["action_description"])
    else:
        print(f"You can't use the {item_to_use.replace('_', ' ')} that way.")


def handle_inventory_command():
    inv = game_state["inventory"]
    if not inv:
        print("Your inventory is empty.")
    else:
        print("\n--- Your Inventory ---")
        for i in inv:
            print(f"- {i.replace('_', ' ')}")
        print("----------------------")


def handle_unknown_command(cmd):
    verb = cmd.get("verb", "that")
    print(f"I don't understand '{verb}'. Try a different command.")


def run_game():
    print("Welcome to the Simple Adventure Game!")
    print("Commands: go [dir], look [item/around], take [item], use [item] on [target], inventory, fight, quit")
    display_current_location()

    while True:
        user_input = input("\nWhat do you do? ").strip()
        if user_input.lower() in ["quit", "exit"]:
            print("Goodbye!")
            sys.exit()

        cmd = parse_input(user_input)
        verb = cmd.get("verb")

        if (game_state["current_location"] == "inside_shack" and
                not game_state["game_flags"]["monster_defeated"] and
                verb not in ["fight", "use", "look", "inventory", "quit"]):
            print("You must deal with the goblin first!")
            continue

        if verb == "go":
            handle_go_command(cmd)
        elif verb == "look":
            handle_look_command(cmd)
        elif verb == "take":
            handle_take_command(cmd)
        elif verb == "use":
            handle_use_command(cmd)
        elif verb == "inventory":
            handle_inventory_command()
        elif verb == "fight":
            if game_state["current_location"] == "inside_shack" and not game_state["game_flags"]["monster_defeated"]:
                combat_encounter("goblin")
            else:
                print("There's nothing to fight here.")
        else:
            handle_unknown_command(cmd)

if __name__ == "__main__":
    run_game()