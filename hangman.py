"""
Hangman 2.1 – fixed IndexError
* lives never exceed available ASCII frames
* difficulty, scoreboard, welcome banner
"""

import random

# ---------------------------------------- CONSTANTS
WORD_LIST = [
    "date", "dune", "gulf", "oasis", "oil", "palm", "pearl", "souk", "spice",
    "tomb", "wadi", "hajj", "camel", "arid", "atlas", "arabian", "bazaar",
    "caravan", "desert", "falcon", "jasmine", "kebab", "lantern", "mirage",
    "minaret", "mosque", "pharaoh", "prophet", "pyramid", "saffron",
    "shawarma", "sultan", "turban", "arabia", "jerusalem", "levantine",
    "mesopotamia", "bedouin", "petroleum", "crusaders", "ramadan",
    "pilgrimage", "sultanate", "desalination", "calligraphy", "geopolitics",
    "hospitality", "marketplace", "cuneiform", "fertilecrescent"
]

HANGMAN_PICS = [
    """
     +---+
         |
         |
         |
        ===
    """,
    """
     +---+
     O   |
         |
         |
        ===
    """,
    """
     +---+
     O   |
     |   |
         |
        ===
    """,
    """
     +---+
     O   |
    /|   |
         |
        ===
    """,
    """
     +---+
     O   |
    /|\\  |
         |
        ===
    """,
    """
     +---+
     O   |
    /|\\  |
    /    |
        ===
    """,
    """
     +---+
     O   |
    /|\\  |
    / \\  |
        ===
    """
]

MAX_FRAMES = len(HANGMAN_PICS) - 1  # 6

# difficulty: (lives, (min_len, max_len))
DIFFICULTY = {
    "easy":   (MAX_FRAMES, (3, 6)),   # 6 lives
    "medium": (MAX_FRAMES, (5, 9)),   # 6 lives
    "hard":   (4,           (7, 20))  # 4 lives
}

wins = losses = 0                     # scoreboard

WELCOME_TEXT = """\
========================================
        H A N G M A N   2.1
========================================
Rules:
1. Guess one letter at a time.
2. Wrong guess → lose a life.
3. Win by revealing the word before lives run out.
Choose a difficulty to begin!
----------------------------------------
"""

# ---------------------------------------- HELPERS
def welcome() -> None:
    print(WELCOME_TEXT)


def get_secret(length_range: tuple[int, int]) -> str:
    pool = [w for w in WORD_LIST if length_range[0] <= len(w) <= length_range[1]]
    return random.choice(pool)


def display_state(secret: str,
                  guessed: set[str],
                  wrong: set[str],
                  lives_left: int) -> None:
    print(HANGMAN_PICS[len(wrong)])
    print("Word:", " ".join(c if c in guessed else "_" for c in secret))
    print("Guessed letters:", " ".join(sorted(guessed | wrong)))
    print("Lives left:", lives_left)
    print("-" * 40)


def get_guess(guessed: set[str], wrong: set[str]) -> str:
    while True:
        g = input("Guess a letter: ").lower()
        if len(g) != 1 or not g.isalpha():
            print("Enter ONE alphabetic letter.")
            continue
        if g in guessed or g in wrong:
            print("Letter already tried.")
            continue
        return g

# ---------------------------------------- GAMEPLAY
def play_round(level: str) -> bool:
    lives, length_range = DIFFICULTY[level]
    secret = get_secret(length_range)
    guessed, wrong = set(), set()

    while True:
        display_state(secret, guessed, wrong, lives - len(wrong))

        if all(c in guessed for c in secret):            # WIN
            print("🎉 You guessed the word:", secret)
            return True

        if len(wrong) >= lives:                          # LOSE
            print("💀 Out of lives! The word was:", secret)
            return False

        g = get_guess(guessed, wrong)
        (guessed if g in secret else wrong).add(g)


def main() -> None:
    global wins, losses
    welcome()

    while True:
        level = ""
        while level not in DIFFICULTY:
            level = input("Choose difficulty (easy / medium / hard): ").lower()

        if play_round(level):
            wins += 1
        else:
            losses += 1

        print(f"🏆 Scoreboard — Wins: {wins} | Losses: {losses}")
        if input("Play again? (y/n): ").lower() != "y":
            print("Thanks for playing! Final score —", wins, "wins &", losses, "losses.")
            break

# ---------------------------------------- MAIN
if __name__ == "__main__":
    main()
