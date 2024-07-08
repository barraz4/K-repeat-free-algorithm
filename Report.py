import numpy as np
import time
import streamlit as st
import Encoder
from Decoder import decode
import SupportFunction


def perform_regression(start_n, final_n, repeat_times, number_of_n):
    n_values = np.linspace(start_n, final_n, number_of_n, dtype=int)
    results = {
        'n': [],
        'k_identical_windows': [],
        'k_identical_windows_ratio': [],
        'runtime': [],
        'logical_errors': []
    }

    progress_bar = st.progress(0)
    total_tasks = len(n_values) * repeat_times
    task_count = 0

    for n in n_values:
        logical_errors = 0
        errors = 0
        total_k_windows = 0
        total_runtime = 0

        for _ in range(repeat_times):
            task_count += 1
            progress_bar.progress(task_count / total_tasks)

            # Reset global counters for each run
            Encoder.reset_identical_windows_count()
            Encoder.reset_logical_error()

            # Generate input sequence and update n
            input_sequence = SupportFunction.generate_input_sequence(n)
            SupportFunction.update_n(input_sequence, from_w=True)

            start_time = time.time()

            # Encoding
            encoded_sequence = Encoder.encode(input_sequence)
            if Encoder.get_logical_error():
                st.write(f"Found a sequence that gave a logical error\n {SupportFunction.original_w}")
                logical_errors += 1
                continue

            # Decoding
            decoded_sequence = decode(encoded_sequence)

            end_time = time.time()

            # Validate results
            if SupportFunction.original_w != decoded_sequence:
                st.write(f"Original and decoded sequences do not match\n{SupportFunction.original_w}\n")
                errors += 1
                continue

            total_k_windows += Encoder.get_identical_windows_count()
            total_runtime += (end_time - start_time)

        total_runs = repeat_times - logical_errors - errors  # we stop a run if logical error occurred
        results['n'].append(n)
        results['k_identical_windows'].append(total_k_windows / total_runs)
        results['k_identical_windows_ratio'].append(total_k_windows / total_runs / n)  # divide by n for normalization
        results['runtime'].append(total_runtime / total_runs)
        results['logical_errors'].append(logical_errors)

    generate_report(results)


def generate_report(results):
    # Generate table
    import pandas as pd
    import altair as alt
    df = pd.DataFrame({
        'n': results['n'],
        'k_identical_windows': results['k_identical_windows'].astype(int),
        'k_identical_windows_ratio': [f"{x:.2e}" for x in results['k_identical_windows_ratio']],
        'runtime[sec]': results['runtime'],
        'logical_errors': results['logical_errors']
    })
    st.table(df)

    # Generate Graphs
    df.set_index('n', inplace=True)
    df['k_identical_windows_ratio'] = df['k_identical_windows_ratio'].astype(float)
    df = df.rename(columns={'runtime[sec]': 'runtime'})  # line_chart had trouble process the title runtime[sec]

    st.write("## k Identical Windows to N Ratio")
    st.line_chart(df['k_identical_windows_ratio'])

    st.write("## Runtime vs n")
    st.line_chart(df['runtime'])

    if df['logical_errors'].sum() > 0:
        st.write("## Logical Errors vs n")
        st.bar_chart(df['logical_errors'])

    df_simplified = pd.DataFrame({
        'n': [1,10,100],
        'runtime': [5, 5.5, 5.591],
    })
