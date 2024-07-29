import SupportFunction
import math


def get_changing_block(expansion_marker=1) -> str:
    return '1' + (2 * SupportFunction.marker + "0" * expansion_marker) + '1'


def is_lyndon(word):
    """
    Determines if the given binary word is a Lyndon word.

    Args:
    word (str): The binary word to check.

    Returns:
    bool: True if the word is a Lyndon word, False otherwise.
    """
    n = len(word)
    # A word of length 1 is always a Lyndon word
    if n == 1:
        return True

    # Compare the word with all its rotations
    for i in range(1, n):
        if word > word[i:] + word[:i]:
            return False
    return True


def generate_binary_lyndon_words_up_to_bits(last_word):
    """
    Generates binary words starting from 1 bit up to max_bits.

    Args:
    max_bits (int): The maximum number of bits for the binary words.

    Returns:
    list: A list of all binary words up to the maximum number of bits.
    """

    min_word = ("0" * (2 * SupportFunction.loglogn - 1) + "1") * SupportFunction.k_tag
    min_val = int(min_word[:SupportFunction.k_tag], 2)

    min_bits = math.ceil(math.log2(min_val))

    if len(last_word) < min_bits:
        last_word = "0" * (min_bits + 1 + (min_bits % 2))

    lyndon_word = ""
    word = last_word
    bits = len(last_word)

    while len(lyndon_word) < SupportFunction.k_tag:
        if int(word, 2) < min_val:
            word = format(min_val, f'0{bits}b')

        while int(word, 2) < ((2 ** bits) - 1):
            if is_lyndon(word) and int(word, 2) >= min_val:
                lyndon_word += word
            word = format(int(word, 2) + 1, f'0{bits}b')
            if len(lyndon_word) > SupportFunction.k_tag:
                break
        if '0' in word:
            word = format(int(word, 2) + 1, f'0{bits}b')
        else:
            bits += 2
            word = format(1, f'0{bits}b')

    return lyndon_word, word


'''

def LengthLimitedLyndonWords(n):
    """Generate nonempty Lyndon words of length <= n over an s-symbol alphabet.
    The words are generated in lexicographic order, using an algorithm from
    J.-P. Duval, Theor. Comput. Sci. 1988, doi:10.1016/0304-3975(88)90113-2.
    As shown by Berstel and Pocchiola, it takes constant average time
    per generated word."""
    w = [-1]                            # set up for first increment
    while w:
        w[-1] += 1                      # increment the last non-z symbol
        yield w
        m = len(w)
        while len(w) < n:               # repeat word to fill exactly n syms
            w.append(w[-m])
        while w and w[-1] == 1:     # delete trailing z's
            w.pop()


def DeBruijnSequence(n):
    """Generate a De Bruijn sequence for words of length n over s symbols
    by concatenating together in lexicographic order the Lyndon words
    whose lengths divide n. The output length will be s^n.
    Because nearly half of the generated sequences will have length
    exactly n, the algorithm will take O(s^n/n) steps, and the bulk
    of the time will be spent in sequence concatenation."""

    output = []
    for w in LengthLimitedLyndonWords(n):
        if n % len(w) == 0:
            output.append(''.join(map(str, w)))
    return sorted(output, key=len)


def cut_Lyndon_words(Lyndon_words: list):
    min_word = ("0" * (2*SupportFunction.loglogn - 1) + "1") * SupportFunction.k_tag
    min_val = int(min_word[:SupportFunction.k_tag], 2)
    i = 0
    while i < len(Lyndon_words):
        if int(Lyndon_words[i], 2) < min_val:
            Lyndon_words.pop(i)
        i += 1
    return Lyndon_words


def concatenating_Lyndon_words(Lyndon_words: list):
    concatenated_lyndon_words = ''.join(Lyndon_words)
    return concatenated_lyndon_words


def build_v_prime() -> str:
    Lyndon_words = DeBruijnSequence(SupportFunction.k_tag)
    remain_Lyndon_words = cut_Lyndon_words(Lyndon_words)
    return concatenating_Lyndon_words(remain_Lyndon_words)


def build_v() -> str:
    v_prime = build_v_prime()
    v = ""
    for i in range(len(v_prime)//SupportFunction.k_tag+1):
        v += v_prime[i*SupportFunction.k_tag:(i+1)*SupportFunction.k_tag] + get_changing_block(expansion_marker=0)
    return v


    '''
