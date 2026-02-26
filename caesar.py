import sys

FREQ = [
    0.08167,  # a
    0.01492,  # b
    0.02782,  # c
    0.04253,  # d
    0.12702,  # e
    0.02228,  # f
    0.02015,  # g
    0.06094,  # h
    0.06966,  # i
    0.00153,  # j
    0.00772,  # k
    0.04025,  # l
    0.02406,  # m
    0.06749,  # n
    0.07507,  # o
    0.01929,  # p
    0.00095,  # q
    0.05987,  # r
    0.06327,  # s
    0.09056,  # t
    0.02758,  # u
    0.00978,  # v
    0.02360,  # w
    0.00150,  # x
    0.01974,  # y
    0.00074,  # z
]


def crack_caesar(cipher: str) -> tuple[str, int, int]:
    """Returns (plaintext, key, corellation)"""
    letters = list("abcdefghijklmnopqrstuvwxyz")
    freqs = []

    # Iterate over every possible key
    for i in range(26):
        delta = 0
        rotated = ""

        # Assemble the rotated string
        for letter in cipher.lower():
            rotated += letters[(i + (ord(letter) - ord("a"))) % 26]

        counts = [0] * 26

        # Count the frequency of each letter in the rotated string
        for letter in rotated:
            counts[ord(letter) - ord("a")] += 1

        # Compute the deviation of plaintext candidate letter frequencies from english frequencies.
        for j in range(26):
            delta += abs(FREQ[j] - (counts[j] / len(rotated)))

        freqs.append((delta, i, rotated))

    # Select the most probable plaintext.
    corellation, key, plaintext = sorted(freqs)[0]
    print(
        f' "{cipher} -> {plaintext}" with correlation {1 - corellation} using key {key}'
    )
    return plaintext, key, corellation


def main(stream=sys.stdin):

    for line in stream:
        # Iterate over every possible key
        crack_caesar(line.rstrip())


if __name__ == "__main__":
    main()
