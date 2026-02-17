from pathlib import Path
import csv
import matplotlib.pyplot as plt


BASE_DIR = Path(__file__).parent
FILE_PATH = BASE_DIR / "matches.csv"
FIELDNAMES = ["map", "agent", "kills", "deaths", "assists"]

matches = []

def load_matches():
    loaded_matches = []

    if not FILE_PATH.exists():
        print("file does not exist")
        return[]

    with open(FILE_PATH, "r", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            row["kills"] = int(row["kills"])
            row["deaths"] = int(row["deaths"])
            row["assists"] = int(row["assists"])
            loaded_matches.append(row)

    return loaded_matches

def append_match(record):
    file_exists = FILE_PATH.exists()

    with open(FILE_PATH, "a+", newline="") as file:
        file.seek(0, 2)  
        is_empty = (file.tell() == 0)

        
        if not is_empty:
            file.seek(file.tell() - 1)
            last_char = file.read(1)
            if last_char != "\n":
                file.write("\n")

        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)

        if is_empty:
            writer.writeheader()

        writer.writerow({
            "map": record["map"],
            "agent": record["agent"],
            "kills": record["kills"],
            "deaths": record["deaths"],
            "assists": record["assists"]
        })

def stats_menu(matches):
    while True:
        print("\n=== View Stats ===")
        print("1) General")
        print("2) By map")
        print("3) By agent")
        print("4) Streak")
        print("5) Graph")
        print("6) Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            show_general_stats(matches)

        elif choice == "2":
            show_stats_by_map(matches)

        elif choice == "3":
            show_stats_by_agent(matches)

        elif choice == "4":
            show_streaks(matches)

        elif choice == "5":
            plot_kd_over_matches(matches)

        elif choice == "6":
            break

        else:
            print("Invalid option. Try again.")

def show_general_stats(matches):
    total_kills = 0
    total_deaths = 0
    total_assists = 0

    for match in matches:
        total_kills += match["kills"]
        total_deaths += match["deaths"]
        total_assists += match["assists"]

    if total_deaths == 0:
        kd = total_kills
        kda = total_kills + total_assists
    else:
        kd = total_kills/total_deaths
        kda = (total_kills + total_assists)/total_deaths

    print("\n=== General Stats ===")
    print("Matches played:", len(matches))
    print("KD:", round(kd, 2))
    print("KAD:", round(kda, 2))

    input("\nPress Enter to return to stats menu...")

def show_stats_by_map(matches):
    target_map = input('which map?').strip().lower()

    totals = {}

    for match in matches:
        if match["map"].strip().lower() == target_map:
            agent = match["agent"].strip()

            if agent not in totals:
                totals[agent] = {"kills": 0, "deaths": 0, "assists": 0}

            totals[agent]["kills"] += match["kills"]
            totals[agent]["deaths"] += match["deaths"]
            totals[agent]["assists"] += match["assists"]

    if len(totals) == 0:
        print("\nNo matches found for that map.")
        input("\nPress Enter to return...")
        return

    print(f"\n=== {target_map.title()} stats by agent ===")

    for agent, data in totals.items():
        if data["deaths"] == 0:
            kd = data["kills"]
            kda = data["kills"] + data["assists"]
        else:
            kd = data["kills"] / data["deaths"]
            kda = (data["kills"] + data["assists"])/ data["deaths"]

        print(f"{agent}: KD {round(kd, 2)} | KAD {round(kda, 2)}")

    input("\nPress Enter to return...")

def show_stats_by_agent(matches):
   target_agent = input("which agent?").strip().lower()
   totals = {}

   for match in matches:
       if match["agent"].strip().lower() == target_agent:
           map_name = match["map"].strip()

           if map_name not in totals:
              totals[map_name] = {"kills": 0, "deaths": 0, "assists": 0}

           totals[map_name]["kills"] += match["kills"]
           totals[map_name]["deaths"] += match["deaths"]
           totals[map_name]["assists"] += match["assists"]

   if len(totals) == 0:
       print("\nNo matches found for that agent.")
       input("\nPress Enter to return...")
       return

   print(f"\n=== {target_agent.title()} stats by map ===")

   for map_name, data in totals.items():
       if data["deaths"] == 0:
           kd = data["kills"]
           kda = data["kills"] + data["assists"]
       else:
           kd = data["kills"]/ data["deaths"]
           kda = (data["kills"]+ data["assists"]) / data["deaths"]

       print(f"{map_name}: KD {round(kd, 2)} | KAD {round(kda, 2)}")
   input("\nPress Enter to return...") 
      
def safe_kd(kills,deaths):
    d = deaths if deaths != 0 else 1
    return kills/d

def safe_kda(kills,deaths,assists):
    if deaths == 0:
        d = 1
    else:
        d = deaths
    return (kills + assists)/d

def match_score(match):
    kd = safe_kd(match["kills"], match["deaths"])
    kda = safe_kda(match["kills"], match["deaths"],match["assists"])
    return (kd + kda)/2

def base_score(matches):
    if len(matches) == 0:
        return 0
    scores = [match_score(m) for m in matches]
    return sum(scores) / len(scores)

def label_from_score(score,base, band=0.20):
    if score >= base + band:
        return "Good"
    elif score <= base-band:
        return "Bad"
    else:
        return "Average"

def get_streak_stats(matches, band=0.20):
    if len(matches) == 0:
       return ("None", 0, 0, 0)
    
    b = base_score(matches)

    current_good = 0
    current_bad = 0
    longest_good = 0
    longest_bad = 0
    mode = ""
    good_hits = 0
    bad_hits = 0
    min_hits = 2

    for m in matches:
        s = match_score(m)
        label = label_from_score(s,b,band=band)

        if label == "Good":
            current_good += 1
            current_bad = 0
            mode = "Good"
            good_hits += 1
            bad_hits = 0
        elif label == "Bad":
            current_bad += 1
            current_good = 0
            mode = "Bad"
            bad_hits += 1
            good_hits = 0
        else:
            if mode =="Good":
                current_good += 1
                current_bad = 0
                good_hits += 1
                bad_hits = 0
            elif mode == "Bad":
                current_bad += 1
                current_good = 0
                good_hits += 1
                bad_hits = 0
            else:
                current_good = 0
                current_bad = 0
                good_hits = 0
                bad_hits = 0

        if current_good > longest_good and good_hits > min_hits:
            longest_good = current_good
        if current_bad > longest_bad and bad_hits > min_hits:
            longest_bad = current_bad

    if current_good > 0:
       return ("Good", current_good, longest_good, longest_bad)
    elif current_bad > 0:
        return ("Bad", current_bad, longest_good, longest_bad)
    else:
       return ("None", 0, longest_good, longest_bad)  

def show_streaks(matches):
    current_type, current_len, longest_good, longest_bad = get_streak_stats(matches, band=0.20)
    print("\n=== Streaks (strict) ===")
    print(f"Longest Good streak: {longest_good}")
    print(f"Longest Bad streak : {longest_bad}")

    if current_type == "None":
        print("Current streak: None")
    else:
        print(f"Current streak: {current_type} ({current_len})")

    input("\nPress Enter to return...")

def plot_kd_over_matches(matches):
    if len(matches) == 0:
        print("\nNo matches to plot.")
        input("\nPress Enter to return...")
        return
    
    kds = []
    for m in matches:
        kd = safe_kd(m["kills"], m["deaths"])
        kds.append(kd)

    kds_display = clip_outliers(kds, low_pct=5, high_pct=95)
    
    games = list(range(1,len(kds) + 1))
    avg_kd = sum(kds)/ len(kds)

    plt.figure(figsize=(10, 5))
    plt.plot(games, kds_display, marker="o", label="KD (clipped)")
    plt.axhline(avg_kd, linestyle=":", linewidth=2, label=f"Avg KD ({avg_kd:.2f})")

    plt.title("KD Over Matches")
    plt.xlabel("Match number")
    plt.ylabel("KD")
    plt.legend()
    plt.grid(True)
    plt.show()

def clip_outliers(values,low_pct=5,high_pct=95):
    sorted_vals = sorted(values)
    n = len(sorted_vals)

    low_index = int(n * low_pct / 100)
    high_index = int(n * high_pct / 100)

    low_bound = sorted_vals[low_index]
    high_bound = sorted_vals[high_index]

    clipped = []
    for v in values:
        if v < low_bound:
            clipped.append(low_bound)
        elif v > high_bound:
            clipped.append(high_bound)
        else:
            clipped.append(v)

    return clipped

def show_last_n_matches(matches,n):
    if len(matches) == 0:
        print("\nNo matches recorded yet.")
        input("\nPress Enter to return...")
        return
    
    n = min(n,len(matches))
    b = base_score(matches)
    print(f"\n=== Last {n} Matches ===")

    start_index = len(matches) - n
    for i in range(start_index, len(matches)):
        m = matches[i]
        kd = safe_kd(m["kills"],m["deaths"])
        kda = safe_kda(m["kills"], m["deaths"],m["assists"])

        score = match_score(m)
        label = label_from_score(score,b,band=0.20)

        print(
            f'{i+1:>3}) {m["map"]} | {m["agent"]} | '
            f'{m["kills"]}/{m["deaths"]}/{m["assists"]} | '
            f'KD {kd:.2f} | KAD {kda:.2f} | {label}'
        )
        
    input("\nPress Enter to return...")

def rewrite_matches_csv(matches, filepath, fieldnames):
    with open(filepath, "w",newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for m in matches:
            writer.writerow({
                "map": m["map"],
                "agent": m["agent"],
                "kills": m["kills"],
                "deaths": m["deaths"],
                "assists": m["assists"]
            })

def delete_match(matches,filepath,fieldnames):
    if len(matches) == 0:
        print("\nNo matches to delete.")
        input("\nPress Enter to return...")
        return
    
    list_matches(matches,n=20)

    try:
        idx = int(input("Enter match number to delete: ").strip())
    except ValueError:
        print("Invalid number.")
        input("\nPress Enter to return...")
        return
    
    if idx < 1 or idx > len(matches):
        print("That match number does not exist.")
        input("\nPress Enter to return...")
        return
    
    m = matches[idx - 1]
    confirm = input(f'Delete match {idx} ({m["map"]}, {m["agent"]}, {m["kills"]}/{m["deaths"]}/{m["assists"]})? (y/n): ').strip().lower()

    if confirm != "y":
       print("Cancelled.")
       input("\nPress Enter to return...")
       return

    matches.pop(idx - 1)
    rewrite_matches_csv(matches,filepath,fieldnames)

    print("Deleted.")
    input("\nPress Enter to return...")

def list_matches(matches,n=20):
    if len(matches) == 0:
        print("\nNo Matches recorded.")
        return
    n = min(n,len(matches))

    start = len(matches) - n
    print(f"\n=== Showing last {n} matches ===")

    for i in range(start,len(matches)):
        m = matches[i]
        print(f'{i+1:>3}) {m["map"]} | {m["agent"]} | '
              f'{m["kills"]}/{m["deaths"]}/{m["assists"]}')

def edit_match(matches,filepath,fieldnames):
    if len(matches) == 0:
        print("\nNo matches to edit.")
        input("\nPress Enter to return...")
        return
    
    list_matches(matches,n=20)

    try:
        idx = int(input("Enter match number to edit: ").strip())
    except ValueError:
        print("Invalid number.")
        input("\nPress Enter to return...")
        return
    
    if idx < 1 or idx > len(matches):
        print("That match number does not exist.")
        input("\nPress Enter to return...")
        return
    
    m = matches[idx - 1]
    print("\nEditing match:")
    print(f'{idx}) {m["map"]} | {m["agent"]} | {m["kills"]}/{m["deaths"]}/{m["assists"]}')
    print("Press Enter to keep the current value.\n")

    new_map = input(f'Map [{m["map"]}]: ').strip()
    new_agent = input(f'Agent [{m["agent"]}]: ').strip()

    def read_int(prompt, current):
        s = input(f"{prompt} [{current}]: ").strip()

        if s == "":
            return current
     
        try:
            return int(s)
        except ValueError:
            print("Invalid number, keeping current.")
            return current
     
    new_kills = read_int("Kills", m["kills"])
    new_deaths = read_int("Deaths", m["deaths"])
    new_assists = read_int("Assists", m["assists"])

    if new_map != "":
        m["map"] = new_map
    if new_agent != "":
        m["agent"] = new_agent

    m["kills"] = new_kills
    m["deaths"] = new_deaths
    m["assists"] = new_assists

    rewrite_matches_csv(matches, filepath, fieldnames)
    print("\nMatch updated.")
    input("\nPress Enter to return...")

         




matches = load_matches()

while True:
    print("\n=== Valorant Tracker ===")
    print("1) Add match")
    print("2) View Stats")
    print("3) Show Recent Matches")
    print("4) Delete Match")
    print("5) Edit Match")
    print("6) Exit")

    choice = input("Choose an option: ").strip()

    if choice == "1":
        print("Adding a match...")
        map_name = input("Map played: ").strip()
        agent = input("Agent played: ").strip()
        kills = int(input("Kills: "))
        deaths = int(input("Deaths: "))
        assists = int(input("Assists: "))

        record = {
            "map": map_name,
            "agent": agent,
            "kills": kills,
            "deaths": deaths,
            "assists": assists
        }

        b = base_score(matches)
        s = match_score(record)
        label = label_from_score(s,b,band = 0.20)

        print(f"\nAuto-label: {label}")
        print(f"(score {s:.2f} vs base {b:.2f})")

        matches.append(record)
        append_match(record)

        print("Match saved.")

    elif choice == "2":
        stats_menu(matches)

    elif choice == "3":
        n = int(input("How Many Games? "))
        if n > 0:
            show_last_n_matches(matches,n)
        else: print("Invalid Choice. Try Again.")

    elif choice == "4":
        delete_match(matches,FILE_PATH,FIELDNAMES)

    elif choice == "5":
        edit_match(matches, FILE_PATH, FIELDNAMES)

    elif choice == "6":
        print("Goodbye!")
        break

    else:
        print("Invalid choice. Try again.")










