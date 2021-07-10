import sys
from amz import Amazon

tracker = Amazon()

if len(sys.argv) == 2:
    if sys.argv[1] == "-a" or sys.argv[1] == "--add":
        new = input("Please input link to add\n> ")
        print("Checking validity of link...")
        tracker.get_price(new)
    elif sys.argv[1] == "-r" or sys.argv[1] == "--run":
        interval = input("Interval between checks?\n> ")
        try:
            interval = int(interval) 
        except ValueError:
            print("Not a valid number. Using 5")
            interval = 5
        if interval < 5:
            print("Too low. Interval is now 5")
            interval = 5
        print("Price checker is now running! Keep this open in the background to have it notify you!")
        tracker.run(interval)
    elif sys.argv[1] == "-d" or sys.argv[1] == "--delete":
        tracker.delete_price()
    elif sys.argv[1] == "-5":
        tracker.get_free_proxies()
    else:
        print("Unknown arg")
elif len(sys.argv) > 2:
    print("Too many args.")
else:
    print("Arg is required")