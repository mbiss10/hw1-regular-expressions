"""
This file holds utility functions for HW 1 
"""
from typing import List, Tuple
import pprint
import os


def process_dir(directory_path: str, process_file_fn: callable) -> List[Tuple]:
    """ Use the provided process_file_fn to process each of the files in the
    given directory and return a list of all the matches found.

    NOTE: You do not need to and should not modify this function or its
    interface, as any changes made locally to this function will not be used
    by the autograder script.
    """
    results = []
    for filename in os.listdir(directory_path):
        # Skip any files in the directory that start with '.'
        if filename[0] != '.':
            f_guesses = process_file_fn(filename, directory_path)
            results.extend(f_guesses)
    return results


def get_gold(gold_path: str) -> List[Tuple]:
    """ Return a list of tuples of the canonical form
    (filename, type, value) given a path to a tsv file of gold e-mails and
    phone numbers.

    NOTE: You do not need to and should not modify this function or its
    interface, as any changes made locally to this function will not be used
    by the autograder script.
    """
    gold_results = []
    for line in open(gold_path, 'r'):
        gold_results.append(tuple(line.strip().split('|')))
    return gold_results

def score_metrics(guess_set, gold_set):
    # Compute the true positives, false positives, and false negatives
    tp = guess_set.intersection(gold_set)
    fp = guess_set - gold_set
    fn = gold_set - guess_set


    #calculate precision, recall and f1
    precision = len(tp)/(len(tp)+len(fp))
    recall = len(tp)/(len(tp)+len(fn))
    f1 = 2*precision*recall/(precision + recall)
    return f1, recall, precision, tp, fp, fn


def score(guess_matches: List[Tuple], gold_matches: List[Tuple]) -> None:
    """
    Score the user-extracted matches by comparing them to a list of gold
    matches and print the results. The comparison is done by computing the
    true positives, false positives and false negatives (from the set
    intersection and difference).

    NOTE: The scoring is case-insensitive (all of the extracted phone
    numbers/email addresses are converted to lower case before comparing)
    and removes duplicates.

    NOTE: You do not need to and should not modify this function or its
    interface, as any changes made locally to this function will not be used
    by the autograder script.
    """
    # Convert the phone numbers/emails (the guesses and the correct/gold)
    # to lowercase
    guess_matches = [
        (filename, match_type, match_value.lower())
        for (filename, match_type, match_value)
        in guess_matches
    ]

    gold_matches = [
        (filename, match_type, match_value.lower())
        for (filename, match_type, match_value)
        in gold_matches
    ]

    # Remove duplicates by converting the lists to sets
    guess_set = set(guess_matches)
    gold_set = set(gold_matches)

    f1, recall, precision, tp, fp, fn = score_metrics(guess_set, gold_set)

    # Print all of the results nicely
    pp = pprint.PrettyPrinter()
    print("Summary score: ")
    print(f"F1 = {f1}")
    print(f"Precision = {precision}")
    print(f"Recall = {recall}")
    print('N=%d, True positives=%d, False positives=%d, False negatives=%d' % (len(guess_set), len(tp), len(fp), len(fn)))
    print('====='*10)
    print('Guesses (N=%d): ' % len(guess_set))
    # pp.pprint(guess_set)
    # print('Gold (%d): ' % len(gold_set))
    # pp.pprint(gold_set)
    print('False Positives (%d): ' % len(fp))
    pp.pprint(fp)
    print('False Negatives (%d): ' % len(fn))
    pp.pprint(fn)
    print('True Positives (%d): ' % len(tp))
    pp.pprint(tp)
