import streamlit as st
import main


# Title and subtitle
st.title("K Repeat Free")
st.subheader("Algorithm for k=alog(n) with 1<a<2")
st.write("by: Ben Shlomo and Bar Yossipovitch")
st.write("Instructed by: Ohad Elishko")
st.markdown('----')

# Buttons for encode, decode, and report
option = st.radio("Please Choose an Option:", ("Encode", "Decode", "Report"))

if option == "Encode":
    main.encode_word()

elif option == "Decode":
    main.decode_word()

elif option == "Report":
    main.make_report()
