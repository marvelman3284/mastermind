import socket
import pickle


def create_code() -> list[str]:
    possible: list[str] = [
        "red",
        "orange",
        "yellow",
        "green",
        "blue",
        "purple",
        "black",
        "white",
    ]
    code: list[str] = []

    while len(code) != 4:
        if len(code) == 0:
            print("Your current code is empty.")
        else:
            print(f"Current code: {code}")

        print(f"Here are your possible choices for you code:\n {possible}")
        combo = input(
            "What color would you like to add to your code (order does matter)? \n>>> "
        )

        combo = combo.replace(" ", "")

        while combo not in possible:
            combo = input(
                "That's not a valid color!\nWhat color would you like to add to your code (order does matter)? \n>>> "
            )
        code.append(combo)

    return code


def color_code(code: list[str], guess: list[str]) -> list[str]:
    color: list[str] = []
    print(f"For a reminder, here is your set code: {code}")
    for i in guess:
        print(
            f"Is {i} the right color but the wrong place (c), the right place and right color (r) or wrong color (n): "
        )
        c = input(">>> ")
        color.append(c)

    return color


def main():
    HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
    PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()

        with conn:
            print(f"Connected by {addr}")
            code = create_code()
            conn.sendall(pickle.dumps(code))

            for _ in range(10):
                try:
                    guess = pickle.loads(conn.recv(4096))
                    color = color_code(code, guess)
                    conn.sendall(pickle.dumps(color))
                except EOFError:
                    print("You lose! The codebreakers guessed the code!")
                    quit()

            print("You win! The codebreaker didn't guess the code in 10 turns!")
            quit()


if __name__ == "__main__":
    main()
