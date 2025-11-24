import json
import datetime
import time
import threading
import os

TASK_FILE = "tasks.json"


# ---------------------------
# LOAD & SAVE TASKS
# ---------------------------
def load_tasks():
    if not os.path.exists(TASK_FILE):
        return []
    with open(TASK_FILE, "r") as f:
        return json.load(f)


def save_tasks(tasks):
    with open(TASK_FILE, "w") as f:
        json.dump(tasks, f, indent=4)


# ---------------------------
# ADD NEW TASK
# ---------------------------
def add_task():
    task_name = input("Enter task name: ")
    date = input("Enter date (DD-MM-YYYY): ")
    time_input = input("Enter time (HH:MM - 24hr format): ")

    task = {
        "task": task_name,
        "date": date,
        "time": time_input,
        "status": "pending"
    }

    tasks = load_tasks()
    tasks.append(task)
    save_tasks(tasks)

    print("\nTask Added Successfully ✅")
    print(f"Task: {task_name}")
    print(f"Reminder Set For: {date} at {time_input}\n")


# ---------------------------
# REMINDER SYSTEM
# ---------------------------
def reminder_thread():
    while True:
        now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
        tasks = load_tasks()

        for t in tasks:
            task_time = t["date"] + " " + t["time"]

            if t["status"] == "pending" and task_time == now:
                print("\n REMINDER ALERT!")
                print(f"Task: {t['task']}")
                print(f"Time: {t['time']}")
                print("---------------------------")

        time.sleep(30)  # check every 30 sec


# ---------------------------
# VIEW TASKS
# ---------------------------
def view_tasks():
    tasks = load_tasks()

    print("\n------ PENDING TASKS ------")
    for t in tasks:
        if t["status"] == "pending":
            print(f"• {t['task']} | {t['date']} {t['time']}")

    print("\n------ COMPLETED TASKS ------")
    for t in tasks:
        if t["status"] == "completed":
            print(f"• {t['task']} | {t['date']} {t['time']}")

    print()


# ---------------------------
# MARK TASK COMPLETED
# ---------------------------
def mark_completed():
    tasks = load_tasks()
    view_tasks()

    name = input("\nWhich task do you want to mark as completed? Enter task name: ")

    found = False
    for t in tasks:
        if t["task"].lower() == name.lower():
            t["status"] = "completed"
            found = True

    if found:
        save_tasks(tasks)
        print("\nTask marked as COMPLETED ✔\n")
    else:
        print("\nTask not found \n")


# ---------------------------
# MAIN MENU
# ---------------------------
def menu():
    while True:
        print("\n----------------------------")
        print("       TASK SCHEDULER")
        print("----------------------------")
        print("1. Add New Task")
        print("2. View Tasks")
        print("3. Mark Task as Completed")
        print("4. Exit")
        print("----------------------------")

        choice = input("Enter choice: ")

        if choice == "1":
            add_task()
        elif choice == "2":
            view_tasks()
        elif choice == "3":
            mark_completed()
        elif choice == "4":
            print("\nExiting... Bye ")
            break
        else:
            print("Invalid choice! Try again.\n")


# ---------------------------
# RUN PROGRAM + REMINDER
# ---------------------------
if __name__ == "__main__":
    threading.Thread(target=reminder_thread, daemon=True).start()
    menu()