import socket
import pickle
from collections import Counter

def send_guess() -> list[str]:
    poss: list[str] = [
        "red",
        "orange",
        "yellow",
        "green",
        "blue",
        "purple",
        "black",
        "white",
    ]

    guess: list[str] = []
    print(f"It is your turn to try to guess the code. Here are the possibilities:\n{poss}")
    for _ in range(4):
        code = input("What is your guess?(order matters): ")
        guess.append(code)

    return guess


def format_color_codes(color_codes: list[str]):
    color = Counter(color_codes)

    return f"There is/are {color['r']} color(s) that are in the right place. There is/are {color['c']} color(s) that are in the wrong spot. There is/are {color['n']} color(s) that aren't used in the code"




HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    code = pickle.loads(s.recv(4096))

    for _ in range(20):
        guess = send_guess()
        s.sendall(pickle.dumps(guess))
        color = pickle.loads(s.recv(4096))
        print(format_color_codes(color))
        if guess == code: 
            print("You win! You guessed the code!")
            break

    print("You lose! You failed to guess the code in 20 turns!")
    quit()

