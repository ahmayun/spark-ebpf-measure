import sys
import random
import math

def main():
    # Check if enough arguments are provided
    if len(sys.argv) < 3:
        print("Usage: python permute.py N item1 item2 ...")
        sys.exit(1)

    # First argument after the script name is the number of permutations
    try:
        num_permutations = int(sys.argv[1])
    except ValueError:
        print("First argument must be an integer representing the number of permutations.")
        sys.exit(1)

    # Remaining arguments are the list items to permute
    items = sys.argv[2:]

    # Calculate the maximum number of unique permutations
    max_permutations = math.factorial(len(items))

    # If requested more than possible, adjust to maximum
    if num_permutations > max_permutations:
        num_permutations = max_permutations

    # To store unique permutations
    seen_permutations = set()

    # Generate unique permutations
    while len(seen_permutations) < num_permutations:
        random.shuffle(items)
        # Convert list to tuple to store in a set
        perm_tuple = tuple(items)
        if perm_tuple not in seen_permutations:
            seen_permutations.add(perm_tuple)
            print(",".join(items))

if __name__ == "__main__":
    main()
