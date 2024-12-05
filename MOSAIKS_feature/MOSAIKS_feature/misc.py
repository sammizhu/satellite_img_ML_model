import pandas as pd

class DuplicateCheck:
    @staticmethod
    def check_duplicates(file_path, subset_columns):
        try:
            data = pd.read_csv(file_path)
            duplicates = data.duplicated(subset=subset_columns, keep=False)
            num_duplicates = duplicates.sum()
            print(f"Total number of duplicate rows based on {subset_columns}: {num_duplicates}")
            return num_duplicates
        except Exception as e:
            print(f"Error checking duplicates: {e}")

class Merge:
    @staticmethod
    def merge_files(file_a, file_b, on_columns, output_file):
        try:
            df_a = pd.read_csv(file_a)
            df_b = pd.read_csv(file_b)
            merged_df = pd.merge(df_a, df_b, on=on_columns, how='inner')
            merged_df.to_csv(output_file, index=False)
            print(f"Successfully merged and saved to {output_file}")
        except Exception as e:
            print(f"Error merging files: {e}")

class Subset:
    @staticmethod
    def fetch_and_save_first_n_rows(input_csv_file_path, output_csv_file_path, n=100):
        try:
            df = pd.read_csv(input_csv_file_path, nrows=n)
            df.to_csv(output_csv_file_path, index=False)
            print(f"First {n} rows saved to {output_csv_file_path}")
        except Exception as e:
            print(f"Error saving first {n} rows: {e}")

class Unique:
    @staticmethod
    def count_distinct_rows(file_path, subset_columns):
        try:
            data = pd.read_csv(file_path)
            distinct_rows = data.drop_duplicates(subset=subset_columns)
            num_distinct = len(distinct_rows)
            print(f"Total number of distinct rows based on {subset_columns}: {num_distinct}")
            return num_distinct
        except Exception as e:
            print(f"Error counting distinct rows: {e}")