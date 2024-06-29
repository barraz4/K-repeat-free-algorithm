import SupportFunction
from Expantion import get_changing_block


def get_compressed_sequence(expended_w: str) -> str:
    """
    remove expansion
    """
    index = expended_w.find(get_changing_block())
    w = expended_w[:index]
    return w


def find_coding_block(w) -> tuple:
    j = w.rfind(SupportFunction.marker)-1
    if j == -2:
        return ()
    f_i = w[j+len(SupportFunction.marker)+2:j+len(SupportFunction.marker)+2+SupportFunction.logn+1]
    f_i = SupportFunction.remove_sequence_validation(f_i)
    i = int(f_i, 2)
    return i, j


def remove_coding_block(w: str, indices: tuple) -> str:
    i, j = SupportFunction.validate_indices(indices)
    word = w[i:i+SupportFunction.k_tag]
    
    if j-i < SupportFunction.k_tag:
        word = (w[i:j] * SupportFunction.k_tag)[:SupportFunction.k_tag]

    w = w[:j] + word + w[j+len(SupportFunction.marker)+SupportFunction.logn+1+3:]
    return w


def decode(expended_w: str) -> str:
    SupportFunction.update_n(expended_w, from_w=False)
    w = get_compressed_sequence(expended_w)
    indices = find_coding_block(w)
    while indices:
        w = remove_coding_block(w, indices)
        indices = find_coding_block(w)
    return SupportFunction.remove_sequence_validation(w)
