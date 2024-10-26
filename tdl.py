def menu():
    print("===Tasks menu===")
    print("1. Add a task")
    print("2. Remove a task")
    print("3. List all tasks")
    print("4. Mark task as completed")
    print("5. Save and exit")

def save_tasks(tasks, filename="tasks.txt"):
    with open(filename, "w") as file:
        for task in tasks:
            file.write(task + "\n")

def load_tasks(filename="tasks.txt"):
    tasks = []
    try:
        with open(filename, "r") as file:
            tasks = [line.strip() for line in file]
    except FileNotFoundError:
        print("Invalid file name. New one will be created.")
    return tasks

def main():
    task_number = 0
    task_to_remove = 0
    tasks = load_tasks()
    while True:
        menu()

        choice = input("Enter your choice: ")
        if choice == "1": #add task
            tasks.append(input("Enter a task: "))
            task_number += 1

        if choice == "2": #remove task
            task_to_remove = int(input("Task index to remove: "))
            tasks.remove(tasks[task_to_remove])

        if choice == "3": #print all tasks
            for i in range(1,len(tasks)):
                if tasks[i] != " ":
                    print(i,".",tasks[i])
            goback = input("Press enter to go back")

        if choice == "4": #mark task as completed
            task_to_complete = int(input("Task index to complete: "))
            tasks[task_to_complete] = tasks[task_to_complete] + " (completed)"

        if choice == "5": #exit
            save_tasks(tasks)
            print("========to do list console by mihai28========")
            break

if __name__ == "__main__":
    main()