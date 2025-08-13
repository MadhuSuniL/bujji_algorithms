"""
String Algorithms Module

This module contains implementations of common string algorithms:
- Palindrome Check
- Anagram Detection
- Rabin-Karp Pattern Matching
- KMP (Knuth-Morris-Pratt) Pattern Matching
- Z-Algorithm Pattern Matching
- Longest Palindromic Substring
- Manacher's Algorithm (Optimized Longest Palindromic Substring)
- String Compression

Each function has clear docstrings explaining usage, inputs, outputs, and complexity.
"""


def is_palindrome(s: str, ignore_case: bool = False, ignore_spaces: bool = False) -> bool:
    """
    Check if the given string is a palindrome.

    Args:
        s (str): Input string.
        ignore_case (bool): If True, ignore case during check.
        ignore_spaces (bool): If True, ignore spaces during check.

    Returns:
        bool: True if palindrome, else False.

    Example:
        >>> is_palindrome("Race car", ignore_case=True, ignore_spaces=True)
        True
    """
    if ignore_case:
        s = s.lower()
    if ignore_spaces:
        s = s.replace(" ", "")
    return s == s[::-1]


def are_anagrams(s1: str, s2: str, ignore_case: bool = False, ignore_spaces: bool = False) -> bool:
    """
    Check if two strings are anagrams (permutations) of each other.

    Args:
        s1 (str): First string.
        s2 (str): Second string.
        ignore_case (bool): If True, ignore case.
        ignore_spaces (bool): If True, ignore spaces.

    Returns:
        bool: True if anagrams, else False.

    Example:
        >>> are_anagrams("Listen", "Silent", ignore_case=True)
        True
    """
    if ignore_case:
        s1 = s1.lower()
        s2 = s2.lower()
    if ignore_spaces:
        s1 = s1.replace(" ", "")
        s2 = s2.replace(" ", "")
    return sorted(s1) == sorted(s2)


def rabin_karp(text: str, pattern: str, prime: int = 101) -> list[int]:
    """
    Rabin-Karp pattern matching algorithm.

    Args:
        text (str): Text string to search in.
        pattern (str): Pattern string to search for.
        prime (int): Prime number for hash modulo to reduce collisions.

    Returns:
        list[int]: List of starting indices where pattern is found.

    Example:
        >>> rabin_karp("abracadabra", "abra")
        [0, 7]

    Complexity:
        Average: O(n + m), Worst: O(n*m) due to collisions.
    """
    n, m = len(text), len(pattern)
    if m > n:
        return []
    base = 256  # number of possible characters (extended ASCII)
    pattern_hash = 0
    text_hash = 0
    h = 1  # base^(m-1) % prime

    for i in range(m-1):
        h = (h * base) % prime

    # Initial hash values
    for i in range(m):
        pattern_hash = (base * pattern_hash + ord(pattern[i])) % prime
        text_hash = (base * text_hash + ord(text[i])) % prime

    occurrences = []

    for i in range(n - m + 1):
        if pattern_hash == text_hash:
            # Confirm by direct comparison to avoid false positives due to hash collision
            if text[i:i+m] == pattern:
                occurrences.append(i)
        if i < n - m:
            text_hash = (base * (text_hash - ord(text[i]) * h) + ord(text[i + m])) % prime
            if text_hash < 0:
                text_hash += prime

    return occurrences


def kmp_search(text: str, pattern: str) -> list[int]:
    """
    Knuth-Morris-Pratt (KMP) pattern matching algorithm.

    Args:
        text (str): Text string to search in.
        pattern (str): Pattern string to search for.

    Returns:
        list[int]: List of starting indices where pattern is found.

    Example:
        >>> kmp_search("ababcabcabababd", "ababd")
        [10]

    Complexity:
        O(n + m), where n = len(text), m = len(pattern)
    """
    def compute_lps(pattern: str) -> list[int]:
        lps = [0] * len(pattern)
        length = 0  # length of the previous longest prefix suffix
        i = 1
        while i < len(pattern):
            if pattern[i] == pattern[length]:
                length += 1
                lps[i] = length
                i += 1
            else:
                if length != 0:
                    length = lps[length-1]
                else:
                    lps[i] = 0
                    i += 1
        return lps

    lps = compute_lps(pattern)
    i = 0  # index for text
    j = 0  # index for pattern
    occurrences = []

    while i < len(text):
        if pattern[j] == text[i]:
            i += 1
            j += 1
        if j == len(pattern):
            occurrences.append(i - j)
            j = lps[j-1]
        elif i < len(text) and pattern[j] != text[i]:
            if j != 0:
                j = lps[j-1]
            else:
                i += 1
    return occurrences


def z_algorithm_search(text: str, pattern: str) -> list[int]:
    """
    Z-Algorithm for pattern matching.

    Args:
        text (str): Text string.
        pattern (str): Pattern string.

    Returns:
        list[int]: List of starting indices where pattern is found.

    Example:
        >>> z_algorithm_search("abacaba", "aba")
        [0, 4]

    Complexity:
        O(n + m), where n = len(text), m = len(pattern)
    """
    concat = pattern + "$" + text
    Z = [0] * len(concat)
    left, right = 0, 0

    for i in range(1, len(concat)):
        if i <= right:
            Z[i] = min(right - i + 1, Z[i - left])
        while i + Z[i] < len(concat) and concat[Z[i]] == concat[i + Z[i]]:
            Z[i] += 1
        if i + Z[i] - 1 > right:
            left, right = i, i + Z[i] - 1

    occurrences = []
    m = len(pattern)
    for i in range(m+1, len(concat)):
        if Z[i] == m:
            occurrences.append(i - m - 1)
    return occurrences


def longest_palindromic_substring(s: str) -> str:
    """
    Finds the longest palindromic substring in s using expand-around-center.

    Args:
        s (str): Input string.

    Returns:
        str: Longest palindromic substring.

    Example:
        >>> longest_palindromic_substring("babad")
        'bab'  # or 'aba'

    Complexity:
        O(n^2) time, O(1) space.
    """
    if not s:
        return ""

    def expand_around_center(left: int, right: int) -> str:
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        return s[left+1:right]

    longest = ""
    for i in range(len(s)):
        # odd length palindrome
        odd_pal = expand_around_center(i, i)
        if len(odd_pal) > len(longest):
            longest = odd_pal
        # even length palindrome
        even_pal = expand_around_center(i, i+1)
        if len(even_pal) > len(longest):
            longest = even_pal
    return longest


def manacher_algorithm(s: str) -> str:
    """
    Manacher's algorithm to find longest palindromic substring in O(n) time.

    Args:
        s (str): Input string.

    Returns:
        str: Longest palindromic substring.

    Example:
        >>> manacher_algorithm("babad")
        'bab'  # or 'aba'

    Complexity:
        O(n) time, O(n) space.
    """
    if not s:
        return ""

    # Transform string: insert '#' between chars and add sentinels to handle even-length palindromes
    T = '#'.join('^{}$'.format(s))
    n = len(T)
    P = [0] * n
    center = 0
    right = 0

    for i in range(1, n - 1):
        mirror = 2*center - i
        if i < right:
            P[i] = min(right - i, P[mirror])
        # Expand palindrome centered at i
        while T[i + 1 + P[i]] == T[i - 1 - P[i]]:
            P[i] += 1
        # Update center and right boundary
        if i + P[i] > right:
            center, right = i, i + P[i]

    # Find max palindrome length and center index
    max_len, center_index = max((v, i) for i, v in enumerate(P))
    start = (center_index - max_len) // 2  # start index in original string
    return s[start:start + max_len]


def string_compression(s: str) -> str:
    """
    Compresses a string by replacing sequences of repeated characters with the character followed by the count.

    Args:
        s (str): Input string.

    Returns:
        str: Compressed string.

    Example:
        >>> string_compression("aaabbcccc")
        'a3b2c4'

    If compression does not reduce string size, returns original string.
    """
    if not s:
        return ""

    compressed = []
    count = 1
    prev = s[0]

    for char in s[1:]:
        if char == prev:
            count += 1
        else:
            compressed.append(prev + (str(count) if count > 1 else ""))
            prev = char
            count = 1
    compressed.append(prev + (str(count) if count > 1 else ""))

    result = "".join(compressed)
    return result if len(result) < len(s) else s

def rabin_karp_search(text: str, pattern: str) -> list[int]:
    """
    Rabin-Karp algorithm for pattern searching using rolling hash.

    Args:
        text (str): The text in which to search.
        pattern (str): The pattern to search for.

    Returns:
        list[int]: Starting indices where pattern is found in text.

    Example:
        >>> rabin_karp_search("abracadabra", "cada")
        [4]
    """
    if pattern == "" or text == "":
        return []

    d = 256  # Number of characters in input alphabet
    q = 101  # A prime number for modulus
    m = len(pattern)
    n = len(text)
    h = pow(d, m-1) % q
    p = 0  # hash value for pattern
    t = 0  # hash value for text
    result = []

    # Initial hash calculation
    for i in range(m):
        p = (d * p + ord(pattern[i])) % q
        t = (d * t + ord(text[i])) % q

    # Slide over text
    for s in range(n - m + 1):
        if p == t:
            # Check actual characters to avoid collision
            if text[s:s+m] == pattern:
                result.append(s)
        if s < n - m:
            t = (t - h * ord(text[s])) % q
            t = (t * d + ord(text[s + m])) % q
            t = (t + q) % q  # Make sure t is positive
    return result

def manacher_longest_palindrome(s: str) -> str:
    """
    Manacher's algorithm to find the longest palindromic substring in O(n) time.

    Args:
        s (str): Input string.

    Returns:
        str: Longest palindromic substring.

    Example:
        >>> manacher_longest_palindrome("babad")
        'bab'  # or 'aba' is also valid
    """
    if not s:
        return ""

    # Transform s to add separators (#) to handle even-length palindromes uniformly
    t = "#" + "#".join(s) + "#"
    n = len(t)
    p = [0] * n  # Array to hold palindrome radii
    center = 0
    right = 0
    max_len = 0
    max_center = 0

    for i in range(n):
        mirror = 2 * center - i

        if i < right:
            p[i] = min(right - i, p[mirror])

        # Expand palindrome centered at i
        a = i + p[i] + 1
        b = i - p[i] - 1
        while a < n and b >= 0 and t[a] == t[b]:
            p[i] += 1
            a += 1
            b -= 1

        # Update center and right boundary
        if i + p[i] > right:
            center = i
            right = i + p[i]

        # Track max palindrome length
        if p[i] > max_len:
            max_len = p[i]
            max_center = i

    # Extract longest palindrome from original string
    start = (max_center - max_len) // 2
    return s[start:start + max_len]


def real_world_examples():
    """
    String Algorithms Module — Real World Usage Examples
    ====================================================

    1. Palindrome Check
       Scenario:
           Validate user input or DNA sequences to check if they read the same forward and backward.
       Benefit:
           Quick validation in text processing or bioinformatics pipelines.

    2. Anagram Detection
       Scenario:
           Spell checkers or word games to detect if two words contain same letters.
       Benefit:
           Efficient comparison for word-based applications.

    3. Rabin-Karp Search
       Scenario:
           Searching patterns in large documents or logs.
       Benefit:
           Fast substring search with rolling hash, suited for multiple pattern checks.

    4. KMP Algorithm
       Scenario:
           Text editors for find/replace functionality.
       Benefit:
           Guarantees linear time pattern matching, great for real-time editing.

    5. Z-Algorithm
       Scenario:
           String matching in DNA sequences.
       Benefit:
           Preprocessing for fast pattern detection and substring queries.

    6. Longest Palindromic Substring
       Scenario:
           Data cleaning or palindrome-based data compression.
       Benefit:
           Find palindromic sequences efficiently.

    7. Manacher’s Algorithm
       Scenario:
           Optimize palindromic substring search in huge texts.
       Benefit:
           Linear time, suitable for large-scale text analysis.

    8. String Compression
       Scenario:
           Save storage space for logs or repetitive texts.
       Benefit:
           Simple run-length encoding for lightweight compression.

    """
    print(real_world_examples.__doc__)


__all__ = [
    "is_palindrome", "are_anagrams", "rabin_karp_search",
    "kmp_search", "z_algorithm", "longest_palindromic_substring",
    "manacher_longest_palindrome", "string_compression",
    "real_world_examples"
]
