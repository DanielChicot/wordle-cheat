#!/usr/bin/env python

import argparse
import re
from functools import reduce


def main():
    args = arguments()
    words = unmatched(five_letter_words(args.words_file), "[" + args.exclusions + "]")
    words = reduce(lambda accumulation, attempt: matched(words, re.sub('[a-z]', '.', attempt).lower()),
                   args.attempts, words)
    words = reduce(lambda accumulation, attempt: misplaced(attempt, accumulation), args.attempts, words)
    [print(x) for x in words]


def misplaced(attempt, words):
    return reduce(lambda accumulation, pair: unmatched(words, misplaced_letter_pattern(pair[0], pair[1])),
                  misplaced_letters(attempt), words)


def misplaced_letter_pattern(position, letter):
    return '.....'[:position] + letter + '.....'[position + 1:]


def misplaced_letters(attempt):
    misplaced_chars = re.sub('[A-Z]', '.', attempt).lower()
    return [(x, misplaced_chars[x]) for x in range(0, 5) if misplaced_chars[x].isalpha()]


def five_letter_words(words_file):
    with open(words_file) as f:
        return [x.strip() for x in matched(f.readlines(), "[a-z]{5}")]


def matched(words, pattern):
    return filtered(lambda x, y: re.compile(f"^{x}$").search(y), words, pattern)


def unmatched(words, pattern):
    return filtered(lambda x, y: not re.compile(f"^{x}$").search(y), words, pattern)


def filtered(include, words, pattern):
    return [x for x in words if include(pattern, x)]


def arguments():
    parser = argparse.ArgumentParser(prog='Wordle helper', description='Cheat at wordle')
    parser.add_argument('-e', '--exclusions', help='Letters that are not in the solution')
    parser.add_argument('-w', '--words-file', help='Location of the words file', default='/usr/share/dict/words')
    parser.add_argument('attempts', help='efforts made so far', nargs='+')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    main()
