import sys
import pandas as pd
import matplotlib.pyplot as plt

def process_data(file_path, mode, program_filter='Q3'):
    # Read the CSV file
    df = pd.read_csv(file_path)

    # Convert shuffle size from strings to numeric values
    df['SHUFFLE_READ'] = df['SHUFFLE_READ'].apply(lambda x: convert_size(x))
    df['SHUFFLE_WRITE'] = df['SHUFFLE_WRITE'].apply(lambda x: convert_size(x))

    # Split the 'ID' column
    split_columns = df['ID'].str.split('_', expand=True)
    print(split_columns)
    split_columns.columns = ['PROGRAM', 'LEVEL', 'RUN']

    # Combine with the original data
    new_df = pd.concat([split_columns, df.drop(columns=['ID'])], axis=1)

    filtered_df = new_df[new_df['PROGRAM'] == program_filter]

    print(filtered_df)

    # Compute average values by PROGRAM
    df_avg = filtered_df.groupby('LEVEL').agg({
        'TOTAL_JOB_TIME': 'mean',
        'TOTAL_DIFF_SUM': 'mean',
        'SHUFFLE_READ': 'mean',
        'SHUFFLE_WRITE': 'mean'
    }).reset_index()

    print(df_avg)

    # Compute percentage time
    df_avg['PERCENTAGE_TIME'] = (df_avg['TOTAL_DIFF_SUM'] / df_avg['TOTAL_JOB_TIME']) * 100

    # Select the appropriate shuffle size column
    shuffle_col = 'SHUFFLE_READ' if mode == 'read' else 'SHUFFLE_WRITE'

    # Sort the dataframe by shuffle size for a smooth line graph
    df_avg = df_avg.sort_values(by=shuffle_col)

    # Plot the graph
    plt.figure(figsize=(10, 6))
    plt.plot(df_avg[shuffle_col], df_avg['PERCENTAGE_TIME'], marker='o')
    for i, row in df_avg.iterrows():
        plt.annotate(row['LEVEL'], (row[shuffle_col], row['PERCENTAGE_TIME']))
    
    
    plt.xlabel(f'Shuffle {mode.capitalize()} Size (bytes)')
    plt.ylabel('Percentage Time (%)')
    plt.title(f'{program_filter}: Shuffle {mode.capitalize()} Size vs Percentage Time')
    plt.grid(True)
    plt.savefig(f'/home/ahmad/Desktop/bpf-playground/learning-ebpf/chapter3/spark-ebpf-measure/figures/{mode}_{program_filter}')
    plt.show()

def convert_size(size_str):
    size_str = size_str.strip().upper()
    if 'GIB' in size_str:
        return float(size_str.replace('GIB', '').strip()) * (1024 ** 3)
    elif 'MIB' in size_str:
        return float(size_str.replace('MIB', '').strip()) * (1024 ** 2)
    elif 'KIB' in size_str:
        return float(size_str.replace('KIB', '').strip()) * 1024
    elif 'B' in size_str:
        return float(size_str.replace('B', '').strip())
    else:
        raise RuntimeError(f"Unrecognized size {size_str}")

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: script.py <path/to/csv> <program> <read|write>")
        sys.exit(1)

    file_path = sys.argv[1]
    program_filter = sys.argv[2]
    mode = sys.argv[3].lower()

    if mode not in ['read', 'write']:
        print("Second argument must be 'read' or 'write'")
        sys.exit(1)

    process_data(file_path, mode, program_filter)
