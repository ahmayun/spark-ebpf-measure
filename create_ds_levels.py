import os
import sys
import pandas as pd
import glob
import random

def create_output_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

def get_all_csv_files(dataset_path):
    return glob.glob(os.path.join(dataset_path, "*.csv"))

def sample_and_save_data(df, fraction, output_path, dataset_name, version, part_index):
    sampled_df = df.sample(frac=fraction, random_state=42)
    new_dataset_name = f"{dataset_name}_l{version}"
    new_dataset_path = os.path.join(output_path, new_dataset_name)
    create_output_directory(new_dataset_path)
    output_file = os.path.join(new_dataset_path, f"part-{part_index:05d}.csv")
    sampled_df.to_csv(output_file, index=False)
    print(f"Created {output_file}")

def process_dataset(input_dir, output_dir, dataset):
    dataset_path = os.path.join(input_dir, dataset)
    if os.path.isdir(dataset_path):
        all_files = get_all_csv_files(dataset_path)
        if all_files:
            for fraction, version in zip([0.25, 0.5, 0.75, 1.0], range(1, 5)):
                for part_index, file in enumerate(all_files):
                    df = pd.read_csv(file)
                    sample_and_save_data(df, fraction, output_dir, dataset, version, part_index)

def process_datasets(input_dir, output_dir):
    create_output_directory(output_dir)
    for dataset in os.listdir(input_dir):
        process_dataset(input_dir, output_dir, dataset)

def main():
    if len(sys.argv) != 3:
        print("Usage: python script.py <path_to_input_directory> <path_to_output_directory>")
        sys.exit(1)

    input_directory = sys.argv[1]
    output_directory = sys.argv[2]

    process_datasets(input_directory, output_directory)

if __name__ == "__main__":
    main()
