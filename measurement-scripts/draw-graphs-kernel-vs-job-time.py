import pandas as pd
import sys, re
import matplotlib.pyplot as plt

# Sample data

df = pd.read_csv(sys.argv[1])
df['DATASET'] = df['DATASET'].apply(lambda x: re.search('\d+P\.?\d+M', x).group()) # df['DATASET'].str.extract(f'(\dP.+M)')

print(df)

# Group by the 'DATASET' column and calculate mean and count
result_df = df.groupby('DATASET').agg(
    AVG_TOTAL_JOB_TIME=('TOTAL_JOB_TIME', 'mean'),
    AVG_TOTAL_DIFF_SUM=('TOTAL_DIFF_SUM', 'mean'),
    COUNT=('TOTAL_JOB_TIME', 'count')
).reset_index()

# print(result_df)


def plot_data(df, y_column, datasets):
    """
    Plots a line graph with the specified y-axis and datasets on the x-axis.

    :param df: DataFrame containing the data.
    :param y_column: Column name to be used for the y-axis.
    :param datasets: List of dataset names to be included in the plot.
    """
    # Filter the DataFrame for the specified datasets
    filtered_df = df[df['DATASET'].isin(datasets)]
    print(filtered_df)

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(filtered_df['DATASET'], filtered_df[y_column], marker='o', linestyle='-')
    plt.xlabel('Dataset')
    plt.ylabel(y_column)
    plt.title(f'{y_column} per Dataset')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.show()

# plot_data(result_df, 'AVG_TOTAL_DIFF_SUM', ['bigtext-2P2M', 'bigtext-2P4M', 'bigtext-2P8M'])


result_df['PERCENTAGE'] = (result_df['AVG_TOTAL_DIFF_SUM'] / result_df['AVG_TOTAL_JOB_TIME']) * 100
percentage_df = result_df[['DATASET', 'PERCENTAGE']].copy()
# plot_data(percentage_df, 'PERCENTAGE', ['bigtext-2P2M', 'bigtext-2P4M', 'bigtext-2P8M'])
# plot_data(percentage_df, 'PERCENTAGE', ['bigtext-2P2M', 'bigtext-4P2M', 'bigtext-8P2M'])
plot_data(percentage_df, 'PERCENTAGE', ['2P2M', '4P4M', '8P8M'])
# plot_data(percentage_df, 'PERCENTAGE', ['2P.5M', '4P1M', '8P2M'])


