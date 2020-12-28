"""
Problem 23
----------

A perfect number is a number for which the sum of its proper divisors is exactly equal
to the number. For example, the sum of the proper divisors of 28 would be
1 + 2 + 4 + 7 + 14 = 28, which means that 28 is a perfect number.

A number n is called deficient if the sum of its proper divisors is less than n and it
is called abundant if this sum exceeds n.

As 12 is the smallest abundant number, 1 + 2 + 3 + 4 + 6 = 16, the smallest number that
can be written as the sum of two abundant numbers is 24. By mathematical analysis, it
can be shown that all integers greater than 28123 can be written as the sum of two
abundant numbers. However, this upper limit cannot be reduced any further by analysis
even though it is known that the greatest number that cannot be expressed as the sum of
two abundant numbers is less than this limit.

Find the sum of all the positive integers which cannot be written as the sum of two
abundant numbers.
"""

import math

# All numbers greater than 28123 can be written as the sum of two abundant numbers
MAX = 28123

def is_abundant(n):
    """ Return whether n is an abundant number """
    return sum(get_proper_divisors(n)) > n


def get_proper_divisors(n):
    """ Return set of all of the proper divisors of n """
    divisors = [1]
    for i in range(2, int(math.sqrt(n))+1):
        if n % i == 0:
            divisors.append(int(n/i))
            divisors.append(i)
    return set(divisors)


if __name__ == "__main__":
    abundant = [i for i in range(12, MAX+1) if is_abundant(i)]    
    sum_two_abundant = set()

    for i in abundant:
        for j in abundant:
            if i+j > MAX:
                break
            sum_two_abundant.add(i+j)
    
    total = sum(i for i in range(MAX+1) if i not in sum_two_abundant)
    print(total)
