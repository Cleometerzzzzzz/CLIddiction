#!/usr/bin/env python3
import argparse
import json
import os
import time
from datetime import datetime
import random

DATA_FILE = os.path.expanduser("~/.addiction_trackers.json")

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def human_time(seconds):
    minutes, sec = divmod(int(seconds), 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    parts = []
    if days:
        parts.append(f"{days}d")
    if hours:
        parts.append(f"{hours}h")
    if minutes:
        parts.append(f"{minutes}m")
    parts.append(f"{sec}s")
    return " ".join(parts)

def encouragement_message(seconds_since_reset):
    """Returns an encouragement message based on the time since last reset."""
    if seconds_since_reset < 30:
        messages = ["Don't give up.", "Stay strong.", "Well, that sucks.", "Better luck next time?", "Oof."]
    elif seconds_since_reset < 5 * 60:
        messages = ["Keep it up.", "You're doing great.", "Stay strong!"]
    elif seconds_since_reset < 60 * 60:
        messages = ["Nice work! You're doing great!", "You're getting stronger!", "One step at a time."]
    elif seconds_since_reset < 24 * 60 * 60:
        messages = ["You can do this.", "Great Progress.", "Keep the momentum going."]
    elif seconds_since_reset < 7 * 24 * 60 * 60:
        messages = ["Keep pushing.", "So proud of you.", "You can do this. I believe in you."]
    elif seconds_since_reset < 30 * 24 * 60 * 60:
        messages = ["Time flies, doesn't it?'", "You're beating it.", "You got this. I believe in you."]
    else:
        messages = ["Stay strong.", "It's all in the past now.'", "Good Job!"]
    return random.choice(messages)

def new_tracker():
    data = load_data()
    name = input("Tracker name: ").strip()
    if not name:
        print("Invalid name.")
        return
    if name in data:
        print("Tracker already exists.")
        return

    data[name] = {
        "start_time": time.time(),
        "history": [] 
    }
    save_data(data)
    print(f"Created tracker '{name}'")

def list_trackers():
    data = load_data()
    if not data:
        print("No active trackers.")
        return
    print("Active trackers:\n")
    now = time.time()
    for name, tracker in data.items():
        if isinstance(tracker, dict) and "start_time" in tracker:
            time_since_reset = now - tracker["start_time"]
            elapsed = human_time(time_since_reset)
            last_reset = datetime.fromtimestamp(tracker["start_time"]).strftime("%Y-%m-%d %H:%M:%S")
            encouragement = encouragement_message(time_since_reset)
            print(f"{name}")
            print(f"  Time since last reset: {elapsed}")
            print(f"  Last reset: {last_reset}")
            print(f"  {encouragement}")
            print("  Past resets:")
            for i, record in enumerate(tracker["history"][:5]):
                reset_time = datetime.fromtimestamp(record["timestamp"]).strftime("%Y-%m-%d %H:%M:%S")
                print(f"    {i + 1}. {reset_time} - {record['note']}")
            print()
        else:
            print(f"Error: Tracker {name} data is corrupted.")

def choose_tracker(data):
    names = list(data.keys())
    if not names:
        print("No trackers available.")
        return None
    if len(names) == 1:
        return names[0]
    print("Choose tracker:")
    for i, name in enumerate(names, 1):
        print(f"{i}) {name}")
    while True:
        try:
            choice = int(input("> "))
            if 1 <= choice <= len(names):
                return names[choice - 1]
        except:
            pass
        print("Invalid selection.")

def reset_tracker(note=None):
    data = load_data()
    name = choose_tracker(data)
    if not name:
        return
    now = time.time()
    if note:
        # add note to the tracker history
        data[name]["history"].insert(0, {"timestamp": now, "note": note})
    data[name]["start_time"] = now  # now reset the timer
    save_data(data)
    print(f"Reset tracker '{name}'")
    if note:
        print(f"Note added: {note}")
    encouragement = encouragement_message(0)
    print(encouragement)

def main():
    parser = argparse.ArgumentParser(description="Simple CLI addiction tracker")
    parser.add_argument("-n", "--new", action="store_true", help="Create new tracker")
    parser.add_argument("-r", "--reset", action="store_true", help="Reset tracker")
    parser.add_argument("-c", "--comment", type=str, help="Note to add when resetting tracker")
    args = parser.parse_args()
    if args.new:
        new_tracker()
    elif args.reset:
        reset_tracker(args.comment)
    else:
        list_trackers()

if __name__ == "__main__":
    main()
