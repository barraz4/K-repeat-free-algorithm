import SupportFunction
import Expantion

k_identical_windows_count = 0
logical_error = False


def update_identical_windows_count(counted=1):
    global k_identical_windows_count
    k_identical_windows_count += counted


def get_identical_windows_count():
    global k_identical_windows_count
    return k_identical_windows_count


def reset_identical_windows_count():
    global k_identical_windows_count
    k_identical_windows_count = 0


def update_logical_error(indication=True):
    global logical_error
    logical_error = indication


def get_logical_error():
    global logical_error
    return logical_error


def reset_logical_error():
    update_logical_error(indication=False)


def find_identical_k_window(w: str, k) -> tuple:
    # Dictionary to store the windows. decimal representation of the window as key and starting index as item
    seen_k_windows = {}
    for j in range(len(w) - k + 1):
        window_decimal_representation = int(w[j:j + k], 3)  # base 3 is work around, can be change to base 2 after find f(i) and sequence_validation on base 2
        if window_decimal_representation in seen_k_windows:  # return indices in case of identical window
            return seen_k_windows[window_decimal_representation], j
        seen_k_windows[window_decimal_representation] = j  # add window and index in case of unique window

    return ()


def add_encoding_block(w: str, indices: tuple) -> str:
    i, j = SupportFunction.validate_indices(indices)
    len_w = len(w)
    code_block = '1' + SupportFunction.marker + '1' + SupportFunction.fi(i) + '1'
    check_for_logical_error(w, j + len(code_block))
    w = w[:j] + code_block + w[j + SupportFunction.k_tag:]
    if len(w) >= len_w:
        print(f"encoding block didn't shorten the length\n{SupportFunction.original_w}")
    return w


def check_for_logical_error(w: str, code_block_last_index):
    error = w[code_block_last_index:code_block_last_index + len(
        SupportFunction.marker) + 1] == '1' + SupportFunction.marker
    update_logical_error(error)


def need_expansion(w: str) -> bool:
    """
    check if w<n
    """
    return len(w) <= SupportFunction.n


def expansion(w: str) -> str:
    """
    expand compressed series with Lyndon words
    """
    next_word = "0"
    remember = ""
    while need_expansion(w):
        lyndon_expansion, next_word = Expantion.generate_binary_lyndon_words_up_to_bits(next_word)
        remember += lyndon_expansion
        w += remember[:SupportFunction.k_tag] + Expantion.get_changing_block(expansion_marker=0)
        remember = remember[SupportFunction.k_tag:]

    return w


def compression(w: str) -> str:
    """
    Remove duplicates k-size windows by encoding the duplication at index j
    """
    indices = find_identical_k_window(w, SupportFunction.k_tag)
    while indices:
        w = add_encoding_block(w, indices)
        update_identical_windows_count()
        indices = find_identical_k_window(w, SupportFunction.k_tag)
    return w


def validate_encoder(w_encode) -> bool:
    if find_identical_k_window(w_encode, SupportFunction.k) != ():
        print(f"encoder retrieve an encode word that is not k-repeat-free {SupportFunction.original_w}")
    if w_encode.find(Expantion.get_changing_block()) == -1:
        print(f"encoder retrieve an encoded word without changing block {SupportFunction.original_w}")


def encode(w) -> str:
    SupportFunction.update_n(w, from_w=True)
    w_validate = SupportFunction.sequence_validation(w)
    w_compress = compression(w_validate)
    w_encode = w_compress + Expantion.get_changing_block()
    if need_expansion(w_encode):
        w_encode = expansion(w_encode)
    validate_encoder(w_encode)
    return w_encode[:SupportFunction.n]
