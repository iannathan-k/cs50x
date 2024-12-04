import csv
import sys


def main():

    # TODO: Check for command-line usage
    numArgs = len(sys.argv) - 1
    if (numArgs != 2):
        print("Must include csvfile and txtfile names, try again!")
        return
    csvfile = sys.argv[1]
    txtfile = sys.argv[2]

    # TODO: Read database file into a variable
    table = {}
    seqNames = []
    with open(csvfile) as file:
        reader = csv.DictReader(file)

        hasPopulateSeqNames = False
        for row in reader:
            name = row['name']
            values = ()

            for k, v in row.items():
                if k == 'name':
                    continue

                if not hasPopulateSeqNames:
                    seqNames.append(k)

                # Store all values as a tuple
                values = values + (int(v), )

            hasPopulateSeqNames = True

            # track the tuple-of-seq-values in the dict
            table[values] = name

    # TODO: Read DNA sequence file into a variable
    with open(txtfile) as file:
        seq = file.readline()

    # TODO: Find longest match of each STR in DNA sequence
    values = ()
    for seqName in seqNames:
        value = longest_match(seq, seqName)
        values = values + (value, )

    # TODO: Check database for matching profiles
    if (table.get(values) is None):
        print("No match")
    else:
        print(table[values])

    return


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
