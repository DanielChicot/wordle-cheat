#!/usr/bin/env python

import argparse
import re
from functools import reduce

from returns.curry import curry
from returns.pipeline import pipe


def main():
    words_file, exclusions, attempts = arguments()
    [print(word) for word in possibilities(exclusions, attempts)(all_words(words_file))]


@curry
def possibilities(exclusions, attempts):
    return pipe(five_letter_words,
                misses_removed(exclusions),
                direct_hits(attempts),
                wrong_position(attempts))


@curry
def wrong_position(attempts, words):
    return reduce(lambda accumulation, attempt: misplaced(attempt, accumulation), attempts, words)


@curry
def direct_hits(attempts, words):
    return reduce(lambda accumulation, attempt: matched(words, re.sub('[a-z]', '.', attempt).lower()),
                  attempts, words)


@curry
def misses_removed(exclusions, words):
    return unmatched(words, "[" + exclusions + "]")


def misplaced(attempt, words):
    return reduce(lambda accumulation, pair: unmatched(words, misplaced_letter_pattern(pair[0], pair[1])),
                  misplaced_letters(attempt), words)


def misplaced_letter_pattern(position, letter):
    return '.....'[:position] + letter + '.....'[position + 1:]


def misplaced_letters(attempt):
    misplaced_chars = re.sub('[A-Z]', '.', attempt).lower()
    return [(i, misplaced_chars[i]) for i in range(0, 5) if misplaced_chars[i].isalpha()]


def five_letter_words(words):
    return [x for x in matched(words, "[a-z]{5}")]


def all_words(words_file):
    with open(words_file) as f:
        return [x.strip() for x in f.readlines()]


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
    return args.words_file, args.exclusions, args.attempts


if __name__ == '__main__':
    main()
