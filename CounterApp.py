import json
import os.path

with open("help.txt") as f:
    HELP_TEXT = f.read()

weekly_goal = int()
weekly_total = int()
daily_goal = int()
daily_total = int()
days_taken = int()

def fetch_data():
    try:
        with open("goals-and-totals.json", 'r') as f:
            data = json.load(f)
            global weekly_goal, daily_goal, weekly_total, daily_total, days_taken
            weekly_goal = data["weekly_goal"]
            daily_goal = data["daily_goal"]
            weekly_total = data["weekly_total"]
            daily_total = data["daily_total"]
            days_taken = data["days_taken"]
    except FileNotFoundError:
        print("goals-and-totals.json file not found")

def print_data():
    print(f"{'~'*52}")
    print(f"|{'Weekly Total: ':12}{weekly_total:4}/{weekly_goal:4}{'Daily Total:':>19}{daily_total:>4}/{daily_goal:3}|")
    print(f"|{'Day: ':5}{days_taken:4}{' '*41}|")
    daily_success_message="You completed  your daily goal!"
    weekly_success_message=f"Congratulations! You've reached your goal in {days_taken} days!"
    if weekly_total >= weekly_goal:
        print(f"|{weekly_success_message:^50}|")
    elif daily_total >= daily_goal:
        print(f"|{daily_success_message:^50}|")
    print(f"{'~'*52}")
        
def command_handler(command):
    global weekly_goal, weekly_total, daily_goal, daily_total, days_taken
    # general
    if command == "quit":
        quit()
    elif command == "help":
        print(HELP_TEXT)
        return True
    elif command == "display":
        print_data()
        return True
    # new week/day
    elif command == "new week":
        print("are you sure you want to start a new week? (Y/n)")
        response = input()
        if response == "" or response.lower() == "y":
            weekly_total = 0
            daily_total = 0
            days_taken = 0
    elif command == "new day":
        print("are you sure you want to start a new day? (Y/n)")
        response = input()
        if response == "" or response.lower() == "y":
            with open("goals-and-totals.json", 'r') as f:
                data = json.load(f)
                key = f"day{days_taken}_reps"
                data[key] = daily_total
                data["daily_total"] = 0
                data["days_taken"] += 1
            save_data(data)
            return False
    # set goals
    elif command.startswith("reset goals"):
        daily_goal = 600
        weekly_goal = 3000
    elif command.startswith("set daily goal"):
        try:
            value = int(command.split(' ')[3])
            if value < 1:
                print("error: come on, you can't be THAT lazy")
                return True
            if value > weekly_goal:
                print("error: set daily goal <value>, daily goal cannot be more than weekly goal")
                return True
            daily_goal = value
        except:
            print("error: set daily goal <value>, <value> should be of type <int>")
            return True
    elif command.startswith("set weekly goal"):
        try:
            value = int(command.split(' ')[3])
            if value < 1:
                print("error: come on, you can't be THAT lazy")
                return True
            if value < daily_goal:
                print("error: set weekly goal <value>, weekly goal cannot be less than daily goal")
                return True
            weekly_goal = value
        except:
            print("error: set weekly goal <value>, <value> should be of type <int>")
            return True
    # daily operations
    elif command.startswith("add"):
        if command.count('-') > 1:
            print("error: add <value>, please use just one '-'")
            return True
        try:
            value = int(command.split(' ')[1])
            if daily_total + value < 0:
                value = -daily_total
            daily_total += value
            weekly_total += value
        except:
            print("error: add <value>, <value> should be of type <int>")
            return True
    elif command.startswith("sub"):
        if command.count('-') > 1:
            print("error: sub <value>, please use just one '-'")
            return True
        try:
            value = int(command.split(' ')[1])
            if daily_total - value < 0:
                value = daily_total
            daily_total -= value
            weekly_total -= value
        except:
            print("error: sub <value>, <value> should be of type <int>")
            return True
    else:
        print(f"\"{command}\" is not recognized as an internal command. please use command \'help\' to see all available commands")
        return True
    
    save_data()
    

def save_data(data = None):
    with open("goals-and-totals.json", 'w') as f:
        if data is None: data = {
            "weekly_goal": weekly_goal,
            "daily_goal": daily_goal,
            "weekly_total": weekly_total,
            "daily_total": daily_total,
            "days_taken": days_taken
        }
        json.dump(data, f)






if __name__ == '__main__':
    # Welcome
    print(f"\n{'  Welcome to Repitition Counter!  ':*^50}")
    print(f"{'Please type `help` for a list of all available commands':*^50}")
    # create json for first time with default values
    if not os.path.exists("goals-and-totals.json"):
        save_data({
                "weekly_goal": 3000,
                "daily_goal": 600,
                "weekly_total": 0,
                "daily_total": 0,
                "days_taken": 1
            })
    # fetch and print
    fetch_data()
    print_data()
    # finally start the main loop for command execution
    while(True):
        print("\n>>", end='')
        skip_flag = command_handler(input()) # sometimes we don't want to display the data after every command
        if skip_flag: continue
        fetch_data()
        print_data()
    