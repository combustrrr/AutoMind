import kagglehub
import pandas as pd
import os

# Download the dataset
print("Downloading dataset...")
path = kagglehub.dataset_download("nehalbirla/vehicle-dataset-from-cardekho")
print(f"Dataset downloaded to: {path}")

# The path is a directory, find the CSV file inside it.
dataset_path = None
if os.path.isdir(path):
    for file_name in os.listdir(path):
        if file_name.endswith('.csv'):
            dataset_path = os.path.join(path, file_name)
            break
else:
    # Handle case where it might be a file (e.g. zip)
    import zipfile
    if path.endswith('.zip'):
        with zipfile.ZipFile(path, 'r') as zip_ref:
            zip_ref.extractall("data/new_dataset")
            # Find the name of the csv file
            csv_files = [f for f in zip_ref.namelist() if f.endswith('.csv')]
            if csv_files:
                dataset_path = os.path.join("data/new_dataset", csv_files[0])
    else:
        dataset_path = path


if dataset_path and os.path.exists(dataset_path):
    # Inspect the first few rows of the dataset
    print("\nInspecting the new dataset:")
    df = pd.read_csv(dataset_path)
    print(df.head())
    print("\nColumns in the new dataset:")
    print(df.columns)
else:
    print("Could not find the CSV file in the downloaded archive or directory.")

