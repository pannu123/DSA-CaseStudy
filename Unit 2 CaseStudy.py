
users = input("Enter users (comma separated): ").split(",")
users = [user.strip() for user in users]

size = len(users)
matrix = [[0] * size for _ in range(size)]


def get_index(name):
    if name in users:
        return users.index(name)
    return -1


def display_matrix():
    print("\n========== ADJACENCY MATRIX ==========")

    print(f"{'User':<14}", end="")

    for user in users:
        print(f"{user:<14}", end="")

    print()

    for i in range(size):
        print(f"{users[i]:<14}", end="")

        for value in matrix[i]:
            print(f"{value:<14}", end="")

        print()

    print("=" * 60)


def add_friendship():
    first = input("Enter first user: ").strip()
    second = input("Enter second user: ").strip()

    i = get_index(first)
    j = get_index(second)

    if i == -1 or j == -1:
        print("User not found.")
    elif i == j:
        print("A user cannot be friends with themselves.")
    elif matrix[i][j] == 1:
        print("Friendship already exists.")
    else:
        matrix[i][j] = 1
        matrix[j][i] = 1
        print("Friendship added successfully.")


def remove_friendship():
    first = input("Enter first user: ").strip()
    second = input("Enter second user: ").strip()

    i = get_index(first)
    j = get_index(second)

    if i == -1 or j == -1:
        print("User not found.")
    elif matrix[i][j] == 0:
        print("Friendship does not exist.")
    else:
        matrix[i][j] = 0
        matrix[j][i] = 0
        print("Friendship removed successfully.")


def check_friendship():
    first = input("Enter first user: ").strip()
    second = input("Enter second user: ").strip()

    i = get_index(first)
    j = get_index(second)

    if i == -1 or j == -1:
        print("User not found.")
    elif matrix[i][j] == 1:
        print(first, "and", second, "are friends.")
    else:
        print(first, "and", second, "are not friends.")


def show_friends():
    name = input("Enter user name: ").strip()
    i = get_index(name)

    if i == -1:
        print("User not found.")
    else:
        friends = []

        for j in range(size):
            if matrix[i][j] == 1:
                friends.append(users[j])

        if friends:
            print("Friends of", name, ":", ", ".join(friends))
            print("Total friends:", len(friends))
        else:
            print(name, "has no friends yet.")


def mutual_friends():
    first = input("Enter first user: ").strip()
    second = input("Enter second user: ").strip()

    i = get_index(first)
    j = get_index(second)

    if i == -1 or j == -1:
        print("User not found.")
    elif i == j:
        print("Enter two different users.")
    else:
        common = []

        for k in range(size):
            if matrix[i][k] == 1 and matrix[j][k] == 1:
                common.append(users[k])

        if common:
            print("Mutual friends:", ", ".join(common))
        else:
            print("No mutual friends found.")


count = int(input("Enter number of existing friendships: "))

for i in range(count):
    print("\nFriendship", i + 1)

    first = input("Enter first user: ").strip()
    second = input("Enter second user: ").strip()

    a = get_index(first)
    b = get_index(second)

    if a == -1 or b == -1 or a == b:
        print("Invalid friendship. Skipped.")
    else:
        matrix[a][b] = 1
        matrix[b][a] = 1


display_matrix()

while True:
    print("\n===== FRIENDSHIP MANAGEMENT SYSTEM =====")
    print("1. Display Adjacency Matrix")
    print("2. Add Friendship")
    print("3. Remove Friendship")
    print("4. Check Friendship")
    print("5. Show Friends")
    print("6. Find Mutual Friends")
    print("7. Exit")

    choice = input("Enter your choice: ").strip()

    if choice == "1":
        display_matrix()

    elif choice == "2":
        add_friendship()

    elif choice == "3":
        remove_friendship()

    elif choice == "4":
        check_friendship()

    elif choice == "5":
        show_friends()

    elif choice == "6":
        mutual_friends()

    elif choice == "7":
        print("Thank you for using the system!")
        break

    else:
        print("Invalid choice. Please try again.")
