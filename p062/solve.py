import collections
import itertools


def solve():
    """ Find the smallest cube for which exactly five permutations of its digits are cube. """
    cubes_by_signature = collections.defaultdict(list)
    permutations = 5
    digits = 0

    for cube in cubes():
        signature = get_digits_signature(cube)
        cubes_by_signature[signature].append(cube)

        # Check for a solution when we've found all cubes with a given number of digits
        if len(signature) > digits:
            solution = find_smallest_cube(cubes_by_signature, permutations)
            if solution:
                return solution
            digits = len(signature)


def cubes():
    """ Discover all cubes! """
    for i in itertools.count(start=1):
        yield i ** 3


def get_digits_signature(number):
    """
    Return all the digits of a number, sorted smallest to largest
    
    e.g., 10608 -> (0, 0, 1, 6, 8)
    """
    digits_chars = tuple(str(number))
    digits_ints = map(int, digits_chars)
    digits_signature = tuple(sorted(digits_ints))
    return digits_signature


def find_smallest_cube(cubes_by_signature, permutations):
    cube_candidates = []
    for signature, cubes in cubes_by_signature.items():
        if len(cubes) == permutations:
            cube_candidates.append(min(cubes))

    if cube_candidates:
        return min(cube_candidates)


if __name__ == "__main__":
    smallest = solve()
    print(f"The smallest cube with 5 permutations is {smallest}!")


# Answer was 127035954683
