import sys
import time
import os

# ────────────────────────────────────────────────
#                  GLOBAL STATE
# ────────────────────────────────────────────────

current_items = []
current_room_index = 0
player_name = ""
ending = ""
is_lid_open = False
bear_interacted = False
knows_acids = False
chair_used = False
roof_open = False
is_masked = False
is_killed = False
secret_solved = False
outdoor_open = False


# ────────────────────────────────────────────────
#               UI HELPER FUNCTIONS
# ────────────────────────────────────────────────

def slow_print(text, delay=0.038, final_pause=0.9):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    time.sleep(final_pause)
    print()


def draw_title(text, width=54, line_char="═"):
    print(line_char * width)
    print(text.center(width))
    print(line_char * width)
    print()


def draw_subtitle(text):
    print("  " + "─" * 44)
    print(f"  {text}")
    print("  " + "─" * 44)
    print()


def draw_menu_header():
    print("\n" + "-" * 45)
    print("             WHAT DO YOU DO?")
    print("-" * 45)


def draw_menu_option(number, text):
    print(f"  {number} → {text}")


def draw_menu_footer():
    print("-" * 45 + "\n")


def show_inventory():
    draw_subtitle("INVENTORY")
    if not current_items:
        slow_print("  (nothing)", delay=0.02, final_pause=0.5)
    else:
        for item in current_items:
            print(f"  • {item}")
    print()


def describe_room(room_id):
    room_name = room_names.get(room_id, "Unknown Area")
    
    print("\n" + "═" * 62)
    slow_print(f"  {room_name.upper()}", delay=0.018)
    print("═" * 62)
    print()
    
    # Oda bazlı kısa atmosferik giriş
    descriptions = {
        0: "Cold concrete... faint echo of dripping water.",
        1: "Long corridor. Dim light flickers overhead.",
        2: "Deeper now. Air feels heavier here.",
        3: "Kitchen. Rust and old grease in the air.",
        4: "Living room. Furniture covered in dust.",
        5: "Balcony. Cold wind brushes your face.",
        6: "Bathroom. Tiles cracked, mirror foggy.",
        7: "Bedroom. Someone lived here once...",
        8: "Another bedroom. Quieter than the first.",
        9: "Sitting room. Something feels watched.",
        10: "Stairs leading up. They creak under your weight.",
        11: "Upper kitchen. Unused for a long time.",
        12: "Upper bedroom. Bed still made.",
        13: "Upper bathroom. Water drips slowly.",
        14: "Secret room. Hidden... and wrong.",
        15: "Silent bathroom. Too quiet.",
        16: "Basement. Darkness presses in."
    }
    slow_print(descriptions.get(room_id, f"You are in the {room_name.lower()}."))
    
    items_here = room_items.get(room_id, [])
    if items_here:
        print()
        slow_print("  You see:")
        for item in items_here:
            print(f"     • {item}")
    else:
        print()
        slow_print("  Nothing of use remains here...")
    
    print()


# ────────────────────────────────────────────────
#                  ENDINGS
# ────────────────────────────────────────────────

def drowned_ending():
    print("\n" * 2)
    draw_title("THE END", line_char="░")
    slow_print("...", delay=0.20, final_pause=1.5)
    slow_print("You can't breathe anymore.")
    slow_print("Vision blurs... darkness creeps in.")
    print()
    slow_print(" \"Subject's pulse dropping.\" ", delay=0.06)
    slow_print(" \"Hemorrhage uncontrollable.\" ", delay=0.06)
    print()
    slow_print("Eyes snap open.")
    slow_print("You're on a gurney.")
    slow_print("Mouth full of copper taste.")
    print()
    slow_print("You were drowning.")
    slow_print("But this time — it's real.")


def runner_ending():
    draw_title("THE END", line_char="░")
    slow_print("You try to run...")
    slow_print("...but legs refuse to obey.")
    print()
    slow_print(" \"Motor functions collapsed.\" ")
    slow_print(" \"Consciousness persists.\"    ")
    print()
    slow_print("Eyes open.")
    slow_print("Faces behind glass. Watching.")
    print()
    slow_print("You're awake.")
    slow_print("But trapped inside your body.")


def murderer_ending():
    draw_title("THE END", line_char="░")
    slow_print("Knife falls from trembling fingers.")
    slow_print("Too real. Too heavy.")
    print()
    slow_print(" \"Subject terminated.\" ")
    slow_print(" \"Recording complete.\" ")
    print()
    slow_print("Everything fades.")
    slow_print("No more mornings.")


def dead_creep_ending():
    draw_title("THE END", line_char="░")
    slow_print("Silence.")
    slow_print("Body on the floor. Still warm.")
    print()
    slow_print("Monitors flicker to life behind you.")
    slow_print("Kitchen entry... teddy bear flip... mask moment.")
    print()
    slow_print("Voice:")
    slow_print("  \"I knew you'd do exactly this.\"")
    slow_print("  \"I've watched every step.\"")
    print()
    slow_print("One screen turns black.")
    slow_print("Your own face stares back.")
    slow_print("Camera angle — from behind you.")
    print()
    slow_print("Breath on your neck.")
    slow_print("\"Wake up.\"")
    print()
    slow_print("Your room. Computer glow.")
    slow_print("Game menu still open...")
    print()
    slow_print("Chair creaks.")
    slow_print("Corner of the room.")
    slow_print("Someone stands there.")
    slow_print("Watching.")
    slow_print("Smiling.")


def escaper_ending():
    draw_title("THE END", line_char="░")
    slow_print("Door swings open.")
    slow_print("Sunlight burns your eyes.")
    print()
    slow_print(" \"Subject has escaped!\" ")
    print()
    slow_print("For the first time...")
    slow_print("You are really awake.")


# ────────────────────────────────────────────────
#                  ROOMS (ALL 17)
# ────────────────────────────────────────────────

def Entrance():
    global current_room_index, outdoor_open, ending
    current_room_index = 0
    while True:
        describe_room(current_room_index)
        draw_menu_header()
        draw_menu_option(1, "Move")
        draw_menu_option(2, "Interact")
        draw_menu_option(3, "Check inventory")
        if "key of to exit" in current_items:
            draw_menu_option(4, "Use exit key")
        draw_menu_footer()
        
        choice = input("  > ").strip()
        
        if choice == "1":
            print("\n  Possible directions:")
            if outdoor_open:
                print("    1 → Corridor")
                print("    2 → Exit door")
            else:
                print("    1 → Corridor")
            try:
                dest = int(input("  > "))
                if dest == 1:
                    return 1
                if dest == 2 and outdoor_open:
                    ending = "the great escaper"
                    return None
            except:
                pass
            slow_print("  That way is not possible.")
            
        elif choice == "2":
            slow_print("  Nothing here to interact with.")
        elif choice == "3":
            show_inventory()
        elif choice == "4" and "key of to exit" in current_items:
            outdoor_open = True
            slow_print("  You turned the key. The exit is now accessible.")
        else:
            slow_print("  Invalid choice.")


def Corridor():
    global current_room_index
    current_room_index = 1
    while True:
        describe_room(current_room_index)
        draw_menu_header()
        draw_menu_option(1, "Move")
        draw_menu_option(2, "Interact")
        draw_menu_option(3, "Check inventory")
        draw_menu_footer()
        
        choice = input("  > ").strip()
        
        if choice == "1":
            print("\n  Where to?")
            print("    1 → Entrance")
            print("    2 → Bathroom")
            print("    3 → Deep corridor")
            print("    4 → Kitchen")
            print("    5 → Living room")
            try:
                dest = int(input("  > "))
                return {1:0, 2:6, 3:2, 4:3, 5:4}.get(dest)
            except:
                slow_print("  Invalid direction.")
        elif choice == "2":
            slow_print("  Nothing to interact with here.")
        elif choice == "3":
            show_inventory()
        else:
            slow_print("  Invalid choice.")


def Deep_Corridor():
    global current_room_index
    current_room_index = 2
    while True:
        describe_room(current_room_index)
        draw_menu_header()
        draw_menu_option(1, "Move")
        draw_menu_option(2, "Interact")
        draw_menu_option(3, "Check inventory")
        draw_menu_footer()
        
        choice = input("  > ").strip()
        
        if choice == "1":
            print("\n  Where to?")
            print("    1 → Bedroom 1")
            print("    2 → Bedroom 2")
            print("    3 → Sitting room")
            print("    4 → Corridor")
            try:
                dest = int(input("  > "))
                return {1:7, 2:8, 3:9, 4:1}.get(dest)
            except:
                slow_print("  Invalid direction.")
        elif choice == "2":
            slow_print("  Nothing here.")
        elif choice == "3":
            show_inventory()
        else:
            slow_print("  Invalid choice.")


def Kitchen():
    global current_room_index, is_lid_open
    current_room_index = 3
    while True:
        describe_room(current_room_index)
        draw_menu_header()
        draw_menu_option(1, "Move")
        draw_menu_option(2, "Interact / Pick up")
        draw_menu_option(3, "Check inventory")
        if "crowbar" in current_items:
            draw_menu_option(4, "Pry lid with crowbar")
        draw_menu_footer()
        
        choice = input("  > ").strip()
        
        if choice == "1":
            print("\n  Where to?")
            print("    1 → Corridor", end="")
            if is_lid_open:
                print("   2 → Hidden room")
            print()
            try:
                dest = int(input("  > "))
                if dest == 1: return 1
                if dest == 2 and is_lid_open: return 14
            except:
                pass
            slow_print("  Can't go there.")
            
        elif choice == "2":
            items = room_items.get(3, [])
            if not items:
                slow_print("  Nothing left here.")
            else:
                for i, item in enumerate(items, 1):
                    print(f"    {i}. {item}")
                try:
                    idx = int(input("  > ")) - 1
                    item = room_items[3].pop(idx)
                    current_items.append(item)
                    slow_print(f"  You take the {item}.")
                except:
                    slow_print("  Wrong choice.")
                    
        elif choice == "3":
            show_inventory()
            
        elif choice == "4" and "crowbar" in current_items:
            slow_print("  You force the lid open.")
            slow_print("  Something waits inside...")
            is_lid_open = True
        else:
            slow_print("  Invalid choice.")


def Living_Room():
    global current_room_index, knows_acids
    current_room_index = 4
    while True:
        describe_room(current_room_index)
        draw_menu_header()
        draw_menu_option(1, "Move")
        draw_menu_option(2, "Read book")
        draw_menu_option(3, "Check inventory")
        draw_menu_footer()
        
        choice = input("  > ").strip()
        
        if choice == "1":
            print("\n  Where to?")
            print("    1 → Corridor")
            print("    2 → Balcony")
            try:
                dest = int(input("  > "))
                if dest == 1: return 1
                if dest == 2: return 5
            except:
                pass
            slow_print("  Can't go there.")
            
        elif choice == "2":
            slow_print("You open the book...")
            if knows_acids:
                slow_print("  You already studied this.")
            else:
                slow_print("  You learn about acids and bases.")
                knows_acids = True
                
        elif choice == "3":
            show_inventory()
        else:
            slow_print("  Invalid choice.")


def Balcony():
    global current_room_index
    current_room_index = 5
    while True:
        describe_room(current_room_index)
        draw_menu_header()
        draw_menu_option(1, "Move")
        draw_menu_option(2, "Pick up")
        draw_menu_option(3, "Check inventory")
        draw_menu_footer()
        
        choice = input("  > ").strip()
        
        if choice == "1":
            print("\n  Where to?")
            print("    1 → Living room")
            try:
                if int(input("  > ")) == 1: return 4
            except:
                pass
            slow_print("  Can't go there.")
            
        elif choice == "2":
            items = room_items.get(5, [])
            if items:
                item = items.pop(0)
                current_items.append(item)
                slow_print(f"  You take the {item}.")
            else:
                slow_print("  Nothing here.")
                
        elif choice == "3":
            show_inventory()
        else:
            slow_print("  Invalid choice.")


def Bathroom():
    global current_room_index
    current_room_index = 6
    while True:
        describe_room(current_room_index)
        draw_menu_header()
        draw_menu_option(1, "Move")
        draw_menu_option(2, "Pick up")
        draw_menu_option(3, "Check inventory")
        draw_menu_footer()
        
        choice = input("  > ").strip()
        
        if choice == "1":
            print("\n  Where to?")
            print("    1 → Corridor")
            try:
                if int(input("  > ")) == 1: return 1
            except:
                pass
            slow_print("  Can't go there.")
            
        elif choice == "2":
            items = room_items.get(6, [])
            if items:
                item = items.pop(0)
                current_items.append(item)
                slow_print(f"  You take the {item}.")
            else:
                slow_print("  Nothing left.")
                
        elif choice == "3":
            show_inventory()
        else:
            slow_print("  Invalid choice.")


def Bedroom():
    global current_room_index, is_masked, is_killed, secret_solved
    current_room_index = 7
    while True:
        describe_room(current_room_index)
        draw_menu_header()
        draw_menu_option(1, "Move")
        draw_menu_option(2, "Read notebook")
        draw_menu_option(3, "Check inventory")
        if ("key for bed" in current_items and not secret_solved) or \
           ("mask" in current_items and secret_solved) or \
           ("bleach" in current_items and "muriatic acid" in current_items and is_masked):
            draw_menu_option(4, "Use item")
        draw_menu_footer()
        
        choice = input("  > ").strip()
        
        if choice == "1":
            print("\n  Where to?")
            print("    1 → Deep corridor")
            print("    2 → Silent bathroom", end="")
            if secret_solved:
                print("   3 → Hidden basement")
            print()
            try:
                dest = int(input("  > "))
                if dest == 1: return 2
                if dest == 2: return 15
                if dest == 3 and secret_solved: return 16
            except:
                pass
            slow_print("  Can't go there.")
            
        elif choice == "2":
            slow_print("You open the notebook...")
            slow_print("  Pages filled with frantic sketches and notes.")
            slow_print("  It feels like someone was afraid...")
            slow_print("  ...of something inevitable.")
            
        elif choice == "3":
            show_inventory()
            
        elif choice == "4":
            if "key for bed" in current_items and not secret_solved:
                slow_print("  You unlock the secret compartment.")
                current_items.remove("key for bed")
                secret_solved = True
            elif secret_solved and "mask" in current_items:
                slow_print("  You put on the mask.")
                current_items.remove("mask")
                is_masked = True
            elif is_masked and "bleach" in current_items and "muriatic acid" in current_items:
                slow_print("  You mix the chemicals...")
                slow_print("  Toxic gas fills the air.")
                current_items.remove("bleach")
                current_items.remove("muriatic acid")
                is_killed = True
            else:
                slow_print("  Nothing happens.")
        else:
            slow_print("  Invalid choice.")


def Second_Bedroom():
    global current_room_index
    current_room_index = 8
    while True:
        describe_room(current_room_index)
        draw_menu_header()
        draw_menu_option(1, "Move")
        draw_menu_option(2, "Pick up")
        draw_menu_option(3, "Check inventory")
        draw_menu_footer()
        
        choice = input("  > ").strip()
        
        if choice == "1":
            print("\n  Where to?")
            print("    1 → Deep corridor")
            try:
                if int(input("  > ")) == 1: return 2
            except:
                pass
            slow_print("  Can't go there.")
            
        elif choice == "2":
            items = room_items.get(8, [])
            if items:
                item = items.pop(0)
                current_items.append(item)
                slow_print(f"  You take the {item}.")
            else:
                slow_print("  Nothing here.")
                
        elif choice == "3":
            show_inventory()
        else:
            slow_print("  Invalid choice.")


def Sitting_Room():
    global current_room_index, chair_used, roof_open, bear_interacted
    current_room_index = 9
    while True:
        describe_room(current_room_index)
        if not bear_interacted:
            slow_print("  A teddy bear sits in the corner, eyes faintly glowing red.")
        draw_menu_header()
        draw_menu_option(1, "Move")
        draw_menu_option(2, "Interact with bear" if not bear_interacted else "Interact")
        draw_menu_option(3, "Check inventory")
        if ("chair" in current_items or chair_used) and not roof_open:
            draw_menu_option(4, "Reach up / open hatch")
        draw_menu_footer()
        
        choice = input("  > ").strip()
        
        if choice == "1":
            print("\n  Where to?")
            print("    1 → Deep corridor", end="")
            if roof_open:
                print("   2 → Stairs up")
            print()
            try:
                dest = int(input("  > "))
                if dest == 1: return 2
                if dest == 2 and roof_open: return 10
            except:
                pass
            slow_print("  Can't go there.")
            
        elif choice == "2":
            if bear_interacted:
                slow_print("  Nothing more here.")
            else:
                bear_interacted = True
                slow_print("  The bear is cute... but its eyes glow red.")
                slow_print("  You feel watched. You flip it over in fear.")
                
        elif choice == "3":
            show_inventory()
            
        elif choice == "4":
            if "chair" in current_items:
                slow_print("  You place the chair under the hatch.")
                current_items.remove("chair")
                chair_used = True
            elif chair_used and not roof_open:
                slow_print("  You pull the hatch open.")
                roof_open = True
            else:
                slow_print("  Nothing to do here.")
        else:
            slow_print("  Invalid choice.")


def Stairs():
    global current_room_index
    current_room_index = 10
    while True:
        describe_room(current_room_index)
        draw_menu_header()
        draw_menu_option(1, "Move")
        draw_menu_option(2, "Interact")
        draw_menu_option(3, "Check inventory")
        draw_menu_footer()
        
        choice = input("  > ").strip()
        
        if choice == "1":
            print("\n  Where to?")
            print("    1 → Sitting room")
            print("    2 → Upper kitchen")
            try:
                dest = int(input("  > "))
                if dest == 1: return 9
                if dest == 2: return 11
            except:
                pass
            slow_print("  Can't go there.")
            
        elif choice == "2":
            slow_print("  Nothing to interact with.")
        elif choice == "3":
            show_inventory()
        else:
            slow_print("  Invalid choice.")


def Upper_Kitchen():
    global current_room_index
    current_room_index = 11
    while True:
        describe_room(current_room_index)
        draw_menu_header()
        draw_menu_option(1, "Move")
        draw_menu_option(2, "Interact")
        draw_menu_option(3, "Check inventory")
        draw_menu_footer()
        
        choice = input("  > ").strip()
        
        if choice == "1":
            print("\n  Where to?")
            print("    1 → Stairs")
            print("    2 → Upper bedroom")
            try:
                dest = int(input("  > "))
                if dest == 1: return 10
                if dest == 2: return 12
            except:
                pass
            slow_print("  Can't go there.")
            
        elif choice == "2":
            slow_print("  Nothing here.")
        elif choice == "3":
            show_inventory()
        else:
            slow_print("  Invalid choice.")


def Upper_Bedroom():
    global current_room_index
    current_room_index = 12
    while True:
        describe_room(current_room_index)
        draw_menu_header()
        draw_menu_option(1, "Move")
        draw_menu_option(2, "Pick up")
        draw_menu_option(3, "Check inventory")
        draw_menu_footer()
        
        choice = input("  > ").strip()
        
        if choice == "1":
            print("\n  Where to?")
            print("    1 → Upper kitchen")
            print("    2 → Upper bathroom")
            try:
                dest = int(input("  > "))
                if dest == 1: return 11
                if dest == 2: return 13
            except:
                pass
            slow_print("  Can't go there.")
            
        elif choice == "2":
            items = room_items.get(12, [])
            if items:
                item = items.pop(0)
                current_items.append(item)
                slow_print(f"  You take the {item}.")
            else:
                slow_print("  Nothing here.")
                
        elif choice == "3":
            show_inventory()
        else:
            slow_print("  Invalid choice.")


def Upper_Bathroom():
    global current_room_index
    current_room_index = 13
    while True:
        describe_room(current_room_index)
        draw_menu_header()
        draw_menu_option(1, "Move")
        draw_menu_option(2, "Pick up")
        draw_menu_option(3, "Check inventory")
        draw_menu_footer()
        
        choice = input("  > ").strip()
        
        if choice == "1":
            print("\n  Where to?")
            print("    1 → Upper bedroom")
            try:
                if int(input("  > ")) == 1: return 12
            except:
                pass
            slow_print("  Can't go there.")
            
        elif choice == "2":
            items = room_items.get(13, [])
            if items:
                item = items.pop(0)
                current_items.append(item)
                slow_print(f"  You take the {item}.")
            else:
                slow_print("  Nothing left.")
                
        elif choice == "3":
            show_inventory()
        else:
            slow_print("  Invalid choice.")


def Secret_Room():
    global current_room_index
    current_room_index = 14
    interactables = ["note 1", "note 2", "note 3"]
    while True:
        describe_room(current_room_index)
        visible = room_items.get(14, []) + interactables
        if visible:
            slow_print("  Visible: " + ", ".join(visible))
        draw_menu_header()
        draw_menu_option(1, "Move")
        draw_menu_option(2, "Interact / Read")
        draw_menu_option(3, "Check inventory")
        draw_menu_footer()
        
        choice = input("  > ").strip()
        
        if choice == "1":
            print("\n  Where to?")
            print("    1 → Kitchen")
            try:
                if int(input("  > ")) == 1: return 3
            except:
                pass
            slow_print("  Can't go there.")
            
        elif choice == "2":
            all_items = room_items.get(14, []) + interactables
            if not all_items:
                slow_print("  Nothing here.")
            else:
                for i, it in enumerate(all_items, 1):
                    print(f"    {i}. {it}")
                try:
                    idx = int(input("  > ")) - 1
                    selected = all_items[idx]
                    if selected in room_items.get(14, []):
                        item = room_items[14].pop(room_items[14].index(selected))
                        current_items.append(item)
                        slow_print(f"  You take the {item}.")
                    elif selected.startswith("note "):
                        note_id = selected.split()[1]
                        if note_id in notes:
                            print("\n" + notes[note_id] + "\n")
                        else:
                            slow_print("  No such note.")
                except:
                    slow_print("  Wrong choice.")
                    
        elif choice == "3":
            show_inventory()
        else:
            slow_print("  Invalid choice.")


def Silent_Bathroom():
    global current_room_index
    current_room_index = 15
    while True:
        describe_room(current_room_index)
        draw_menu_header()
        draw_menu_option(1, "Move")
        draw_menu_option(2, "Pick up")
        draw_menu_option(3, "Check inventory")
        draw_menu_footer()
        
        choice = input("  > ").strip()
        
        if choice == "1":
            print("\n  Where to?")
            print("    1 → Bedroom")
            try:
                if int(input("  > ")) == 1: return 7
            except:
                pass
            slow_print("  Can't go there.")
            
        elif choice == "2":
            items = room_items.get(15, [])
            if items:
                item = items.pop(0)
                current_items.append(item)
                slow_print(f"  You take the {item}.")
            else:
                slow_print("  Nothing here.")
                
        elif choice == "3":
            show_inventory()
        else:
            slow_print("  Invalid choice.")


def Hidden_Basement():
    global ending, current_room_index
    current_room_index = 16
    describe_room(16)
    
    if is_killed:
        slow_print("  A body lies on the floor.")
        slow_print("  Monitors show every room you've been in... and you.")
        slow_print("  He was watching. All along.")
        ending = "dead creep"
    else:
        slow_print("  A figure stands in the shadows.")
        slow_print("  He smiles — too wide.")
        if "knife" in current_items:
            while True:
                print("\n  What now?")
                print("    1 → Run")
                print("    2 → Use knife")
                ch = input("  > ").strip()
                if ch == "1":
                    slow_print("  You turn to flee...")
                    slow_print("  But you're too slow.")
                    ending = "runner"
                    break
                elif ch == "2":
                    slow_print("  You lunge with the knife.")
                    slow_print("  He just... smiles wider.")
                    slow_print("  Then everything goes black.")
                    ending = "murderer"
                    break
                else:
                    slow_print("  Invalid.")
        else:
            slow_print("  He steps closer.")
            slow_print("  Hands around your throat.")
            slow_print("  ...")
            ending = "drowned"


# ────────────────────────────────────────────────
#                  DATA
# ────────────────────────────────────────────────

rooms = {
    0: Entrance, 1: Corridor, 2: Deep_Corridor, 3: Kitchen,
    4: Living_Room, 5: Balcony, 6: Bathroom, 7: Bedroom,
    8: Second_Bedroom, 9: Sitting_Room, 10: Stairs,
    11: Upper_Kitchen, 12: Upper_Bedroom, 13: Upper_Bathroom,
    14: Secret_Room, 15: Silent_Bathroom, 16: Hidden_Basement
}

room_names = {
    0: "Entrance", 1: "Corridor", 2: "Deep Corridor", 3: "Kitchen",
    4: "Living Room", 5: "Balcony", 6: "Bathroom", 7: "Bedroom",
    8: "Second Bedroom", 9: "Sitting Room", 10: "Stairs",
    11: "Upper Kitchen", 12: "Upper Bedroom", 13: "Upper Bathroom",
    14: "Secret Room", 15: "Silent Bathroom", 16: "Hidden Basement"
}

room_items = {
    3: ["knife", "chair"],
    5: ["pickle"],
    6: ["muriatic acid"],
    8: ["mask"],
    12: ["key for bed"],
    13: ["crowbar"],
    14: ["key of to exit"],
    15: ["bleach"]
}

notes = {
    "1": """NOTE 1 — Observation Log

Day 41

You still check corners when you enter a room.
That means you feel me.

I stopped writing the times you sleep.
It felt unfair —
you never get to choose when you wake up anyway.""",
    "2": """NOTE 2 — Personal Reminder

Don’t rush.

The knife makes them brave.
The running makes them hopeful.

Hope lasts exactly 3.4 seconds
after eye contact.""",
    "3": """NOTE 3 — Final Draft

I didn’t build this place to trap you.

I built it to learn you.

Your fear curve is beautiful.

If you’re reading this,
it means you finally reached me.

I’ve been waiting.

Don’t blink."""
}


# ────────────────────────────────────────────────
#                  GAME START
# ────────────────────────────────────────────────

print("Github : https://github.com/catowic")
print("Youtube : https://www.youtube.com/@Catowic")
print("To report errors : https://x.com/catowic")
print("By Catowic .")
print("\nPress Enter to start the game...")
input()
os.system('cls' if os.name == 'nt' else 'clear')

draw_title("ARTRAK", line_char="█")

slow_print("What is your name?")
while True:
    player_name = input("  > ").strip()
    if player_name:
        break
    slow_print("  Name cannot be empty.")
print()
slow_print(f"Welcome, {player_name}...")
time.sleep(1.2)
slow_print("Try to survive.", final_pause=1.8)

while not ending:
    result = rooms[current_room_index]()
    if result is not None:
        current_room_index = result

draw_title("FINAL", line_char="░")

if ending == "drowned":
    drowned_ending()
elif ending == "runner":
    runner_ending()
elif ending == "murderer":
    murderer_ending()
elif ending == "dead creep":
    dead_creep_ending()
elif ending == "the great escaper":
    escaper_ending()

print("\n" + "═" * 62)
slow_print("           GAME OVER")
print("═" * 62)
input("\n  Press Enter to exit...")