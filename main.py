import streamlit as st
import time
from Report import perform_regression
from Encoder import encode, find_identical_k_window
from Decoder import decode
from Expantion import get_changing_block
import SupportFunction


def make_report():
    st.write("Please choose the values for the report:")
    col1, col2 = st.columns(2)
    start_n = col1.number_input("Start n", value=SupportFunction.min_n, min_value=SupportFunction.min_n)
    final_n = col1.number_input("Final n", value=1_000_000, min_value=SupportFunction.min_n)
    repeat_times = col2.number_input("Repeat times", value=5, min_value=1)
    number_of_n = col2.number_input("Number of n", value=25, min_value=1)

    if st.button("Generate Report", key="report_button"):
        perform_regression(start_n, final_n, repeat_times, number_of_n)


def encode_word():
    word = None
    choice = st.radio("please choose encoding input", ("word", "length"))

    if choice == "word":
        input_word = st.text_input(f"Enter a binary word with at least {SupportFunction.min_n} bits:\n")
        if st.button("Submit Word", key="submit_word"):
            if not all(c in "01" for c in input_word):
                st.error(f"word provided is not a binary word, try again")
                return
            if len(input_word) < SupportFunction.min_n:
                st.error(f"word length is {len(input_word)} while min length is {SupportFunction.min_n}, try again")
                return
            word = input_word

    if choice == "length":
        input_length = st.text_input(f"Enter a length >= {SupportFunction.min_n}: ")
        if st.button("Submit Length", key="submit_length"):
            if not input_length.isdigit():
                st.error(f"length provided should be an integer, try again")
                return
            input_length = int(input_length)
            if input_length < SupportFunction.min_n:
                st.error(f"length provided should be at least {SupportFunction.min_n}, try again")
                return
            word = SupportFunction.generate_input_sequence(input_length)

    if word:
        tic = time.time()
        word_encoded = encode(word)
        encoding_time = int(time.time() - tic)

        st.write(f"Took {encoding_time}sec to encode")
        st.write(f"The Encoded word with {SupportFunction.k_tag}-{SupportFunction.k}-Repeat-Free is:")
        with st.expander(f"{word_encoded[:90]}..."):
            st.write(word_encoded)


def decode_word():
    submitted = None
    encoded_word = st.text_input(f"Enter an encoded binary word:\n")
    if st.button("Submit Word", key="submit_word"):
        submitted = True
        if not all(c in "012" for c in encoded_word):
            st.error(f"word provided is not a binary word, try again")
            return
        if len(encoded_word) < SupportFunction.min_n:
            st.error(f"word length is {len(encoded_word)} while min length is {SupportFunction.min_n}, try again")
            return
        SupportFunction.update_n(encoded_word, from_w=False)
        if find_identical_k_window(encoded_word, SupportFunction.k) != ():
            st.error(f"encoded_word is not valid- not a k-repeat-free")
            return
        if encoded_word.find(get_changing_block()) == -1:
            st.error(f"encoded_word is not valid- don't have changing_block")
            return

    if submitted:
        tic = time.time()
        word_decoded = decode(encoded_word)
        decoding_time = int(time.time() - tic)

        st.write(f"Took {decoding_time}sec to decode")
        st.write(f"The Decoded word is:")
        with st.expander(f"{word_decoded[:90]}..."):
            st.write(word_decoded)

