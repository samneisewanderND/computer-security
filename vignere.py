import sys
import re
import collections
from collections import defaultdict
from typing import Generator
from caesar import crack_caesar


def compute_ic(cipher: str) -> float:
    cipher = cipher.lower()
    n = len(cipher)
    freq = [0] * 26

    for letter in cipher:
        i = ord(letter) - ord("a")
        freq[i] += 1

    sigma_total = 0
    for i in range(26):
        sigma_total += freq[i] * (freq[i] - 1)

    ic = (1 / (n * (n - 1))) * sigma_total
    return ic


def find_repeated_substrings(cipher: str) -> Generator[tuple[str, int], None, None]:
    """Yields a substring that appears more than once in a given string, and the distance between repeats."""

    # Maps strings to a int representing the starting index of the last occurence of the string, or -1 if it hasn't been seen before.
    substrings = defaultdict(lambda: -1)
    min_length = 2

    # Iterate through all possible substrings
    for i in range(len(cipher) - min_length + 1):
        for j in range(min_length, len(cipher) - i + 1):
            substring = cipher[i : i + j]
            last_seen = substrings[substring]

            if last_seen > 0:
                yield (substring, i - last_seen)

            substrings[substring] = i


def decode_vignere(cipher: str, keys: list[int]):
    period = len(keys)

    columns = [""] * period
    for i, c in enumerate(cipher.strip().lower()):
        columns[i % period] += c

    plaintext = [""] * len(cipher)

    for i, alphabet in enumerate(columns):
        for j, c in enumerate(alphabet):
            index = ord(c) - ord("a")
            shifted_index = (index + keys[i]) % 26
            shifted_c = chr(ord("a") + shifted_index)

            plaintext[j * period + i] = shifted_c

    print("".join(plaintext))


def analyze_vignere(cipher: str):
    print(f"Index of coincidence: {compute_ic(cipher)}")

    substrings = list(find_repeated_substrings(cipher))
    substrings.sort(key=lambda x: -len(x[0]))

    print("All repeated substrings")
    for substring, gap in substrings:
        print(f"{substring:10} (gap {gap})")

    print()
    key_length = 10
    alphabets = [""] * key_length

    for i in range(len(cipher)):
        alphabets[i % key_length] += cipher[i]

    print(f"Alphabet ICs:")
    for i, alphabet in enumerate(alphabets):
        ic = compute_ic(alphabet)
        print(f"#{(i + 1)}: {ic:.2f}, {"(good)" if ic > .066 else "(bad)"}")

    plaintext = ""
    plain_alphabets = []
    for alphabet in alphabets:
        alph_plaintext, _, _ = crack_caesar(alphabet)
        plain_alphabets.append(alph_plaintext)

    for i in range(len(cipher) // key_length):
        for alphabet in plain_alphabets:
            try:
                plaintext += alphabet[i]
            except IndexError:
                pass

    print(plaintext)


def main(stream=sys.stdin):
    for line in stream:
        cipher = line.strip()
        analyze_vignere(cipher)

        key = [0, 14, 0, 1, 22, 0, 14, 0, 1, 22]
        decode_vignere(cipher, key)

        key_text = "".join([chr(((26 - i) % 26) + ord("a")) for i in key])
        print(key_text)


if __name__ == "__main__":
    main()
