"""
Math Algorithms Module

This module contains common and essential math algorithms used in
number theory, cryptography, and combinatorics with efficient
implementations and clear usage examples.

Algorithms included:
- Prime Check
- GCD / LCM
- Sieve of Eratosthenes
- Fast Exponentiation (Binary Exponentiation)
- Modular Inverse (Extended Euclid & Fermat's Little Theorem)
- Fibonacci (Iterative & Matrix Exponentiation)

Each function has detailed docstrings with usage and complexity info.
"""

def is_prime(n: int) -> bool:
    """
    Check if n is prime using simple trial division.

    Args:
        n (int): Number to check for primality.

    Returns:
        bool: True if prime, False otherwise.

    Time Complexity: O(√n)
    Space Complexity: O(1)

    Example:
        >>> is_prime(17)
        True
        >>> is_prime(18)
        False
    """
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def gcd(a: int, b: int) -> int:
    """
    Compute the Greatest Common Divisor (GCD) of a and b using Euclid's algorithm.

    Args:
        a (int): First integer.
        b (int): Second integer.

    Returns:
        int: GCD of a and b.

    Time Complexity: O(log(min(a,b)))
    Space Complexity: O(1)

    Example:
        >>> gcd(48, 18)
        6
    """
    while b:
        a, b = b, a % b
    return abs(a)


def lcm(a: int, b: int) -> int:
    """
    Compute the Least Common Multiple (LCM) of a and b using GCD.

    Args:
        a (int): First integer.
        b (int): Second integer.

    Returns:
        int: LCM of a and b.

    Time Complexity: O(log(min(a,b)))
    Space Complexity: O(1)

    Example:
        >>> lcm(4, 6)
        12
    """
    return abs(a * b) // gcd(a, b) if a and b else 0


def sieve_of_eratosthenes(n: int) -> list[int]:
    """
    Generate all prime numbers up to n (inclusive) using the sieve of Eratosthenes.

    Args:
        n (int): Upper limit for primes.

    Returns:
        List[int]: List of prime numbers <= n.

    Time Complexity: O(n log log n)
    Space Complexity: O(n)

    Example:
        >>> sieve_of_eratosthenes(10)
        [2, 3, 5, 7]
    """
    if n < 2:
        return []
    sieve = [True] * (n + 1)
    sieve[0], sieve[1] = False, False
    p = 2
    while p * p <= n:
        if sieve[p]:
            for i in range(p * p, n + 1, p):
                sieve[i] = False
        p += 1
    return [i for i, prime in enumerate(sieve) if prime]


def fast_exp(base: int, exponent: int) -> int:
    """
    Compute base raised to the power exponent using binary exponentiation.

    Args:
        base (int): The base number.
        exponent (int): The exponent (non-negative).

    Returns:
        int: base^exponent

    Time Complexity: O(log exponent)
    Space Complexity: O(1)

    Example:
        >>> fast_exp(2, 10)
        1024
    """
    if exponent < 0:
        raise ValueError("Negative exponent not supported in fast_exp.")
    result = 1
    power = base
    exp = exponent
    while exp > 0:
        if exp & 1:
            result *= power
        power *= power
        exp >>= 1
    return result


def extended_gcd(a: int, b: int) -> tuple[int, int, int]:
    """
    Extended Euclidean Algorithm.

    Returns gcd(a,b) and coefficients x,y such that ax + by = gcd(a,b).

    Args:
        a (int): First integer.
        b (int): Second integer.

    Returns:
        tuple: (gcd, x, y)

    Example:
        >>> extended_gcd(30, 20)
        (10, 1, -1)
    """
    if b == 0:
        return (a, 1, 0)
    gcd_val, x1, y1 = extended_gcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return (gcd_val, x, y)


def mod_inverse(a: int, m: int) -> int | None:
    """
    Compute Modular Inverse of a under modulo m using Extended Euclidean Algorithm.

    Args:
        a (int): Number to find inverse for.
        m (int): Modulus.

    Returns:
        int or None: Modular inverse of a mod m if exists, else None.

    Time Complexity: O(log m)
    Space Complexity: O(1)

    Example:
        >>> mod_inverse(3, 11)
        4
        # Because 3 * 4 ≡ 1 (mod 11)
    """
    gcd_val, x, _ = extended_gcd(a, m)
    if gcd_val != 1:
        return None  # Inverse doesn't exist if a and m are not coprime
    return x % m


def fibonacci_iterative(n: int) -> int:
    """
    Compute the nth Fibonacci number iteratively.

    Args:
        n (int): Index (0-based).

    Returns:
        int: nth Fibonacci number.

    Time Complexity: O(n)
    Space Complexity: O(1)

    Example:
        >>> fibonacci_iterative(10)
        55
    """
    if n < 0:
        raise ValueError("Negative index not supported.")
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def fibonacci_matrix(n: int) -> int:
    """
    Calculate the nth Fibonacci number using matrix exponentiation.

    Args:
        n (int): Index of Fibonacci number to compute (0-based).

    Returns:
        int: The nth Fibonacci number.

    Example:
    >>> fibonacci_matrix(0)
    0
    >>> fibonacci_matrix(1)
    1
    >>> fibonacci_matrix(10)
    55
    """
    if n == 0:
        return 0

    def matrix_multiply(A, B):
        return [
            [A[0][0]*B[0][0] + A[0][1]*B[1][0],
             A[0][0]*B[0][1] + A[0][1]*B[1][1]],
            [A[1][0]*B[0][0] + A[1][1]*B[1][0],
             A[1][0]*B[0][1] + A[1][1]*B[1][1]],
        ]

    def matrix_pow(M, power):
        if power == 0:
            # Identity matrix for power 0
            return [[1, 0],
                    [0, 1]]
        if power == 1:
            return M
        half = matrix_pow(M, power // 2)
        half_squared = matrix_multiply(half, half)
        if power % 2 == 0:
            return half_squared
        else:
            return matrix_multiply(half_squared, M)

    F = [[1, 1],
         [1, 0]]
    result = matrix_pow(F, n - 1)
    return result[0][0]


def real_world_examples():
    """
    Math Algorithms Module — Real World Usage Examples
    ==================================================

    1. Prime Check
       Scenario:
           Cryptography, random number generation.
       Benefit:
           Quickly verify prime numbers for secure keys.

    2. GCD / LCM
       Scenario:
           Simplifying fractions or scheduling problems.
       Benefit:
           Fundamental building blocks in number theory.

    3. Sieve of Eratosthenes
       Scenario:
           Finding primes up to large N efficiently.
       Benefit:
           Fast precomputation of primes for multiple queries.

    4. Fast Exponentiation
       Scenario:
           Modular exponentiation in cryptography.
       Benefit:
           Compute large powers quickly with binary exponentiation.

    5. Modular Inverse
       Scenario:
           Cryptographic algorithms like RSA.
       Benefit:
           Enables division in modular arithmetic.

    6. Fibonacci Number Generation
       Scenario:
           Mathematical modeling and algorithm challenges.
       Benefit:
           Efficient computation with iterative or matrix methods.

    """
    print(real_world_examples.__doc__)


__all__ = [
    "is_prime", "gcd", "lcm", "sieve_of_eratosthenes",
    "fast_exponentiation", "modular_inverse", "fibonacci_iterative",
    "fibonacci_matrix", "real_world_examples"
]
