import pandas as pd
import os
import sys

def reduce_csv_size_to_plain_csv(file_path, max_size_mb=24, initial_sample_ratio=1.0, encoding='utf-8'):
    """
    Reads a CSV, samples rows if necessary, and saves it as an uncompressed CSV,
    overwriting the original file if reduction is needed.
    This version ensures the final output is a plain CSV and skips type optimization.
    """
    max_size_bytes = max_size_mb * 1024 * 1024

    if not os.path.exists(file_path):
        print(f"  Error: CSV file not found at {file_path}")
        return False, "File not found"

    current_size_mb = os.path.getsize(file_path) / (1024 * 1024)
    print(f"  Checking '{os.path.basename(file_path)}'. Current size: {current_size_mb:.2f} MB")

    if current_size_mb <= max_size_mb:
        print(f"  '{os.path.basename(file_path)}' is already within the {max_size_mb} MB limit. No reduction needed.")
        return True, "No reduction needed"

    print(f"  '{os.path.basename(file_path)}' exceeds {max_size_mb} MB. Attempting to reduce size by row deletion...")

    # Step 1: Load data
    try:
        df = pd.read_csv(file_path, encoding=encoding)
        print(f"  Original DataFrame has {len(df)} rows and {len(df.columns)} columns.")
    except Exception as e:
        print(f"  Error reading CSV '{os.path.basename(file_path)}': {e}")
        return False, f"Error reading CSV: {e}"

    # Step 2: Sample rows if needed, then save as uncompressed CSV and check size
    current_sample_ratio = initial_sample_ratio
    original_row_count = len(df)

    # Calculate the approximate ratio needed to reach the target size
    # This helps in making the initial sampling more aggressive if the file is very large
    approx_required_ratio = max_size_mb / current_size_mb
    if approx_required_ratio < initial_sample_ratio:
        current_sample_ratio = max(0.01, approx_required_ratio * 1.1) # Add a small buffer, min 1%

    while True:
        if current_sample_ratio < 1.0:
            # Sample rows if we're iterating due to oversized file
            df_to_save = df.sample(frac=current_sample_ratio, random_state=42).reset_index(drop=True)
            print(f"  Sampling {current_sample_ratio*100:.2f}% of original rows ({len(df_to_save)} rows).")
        else:
            df_to_save = df # Use the full DataFrame initially

        try:
            # Save directly as uncompressed CSV, overwriting the original
            df_to_save.to_csv(file_path, index=False, encoding=encoding)
            final_size = os.path.getsize(file_path) / (1024 * 1024)
            print(f"  Saved (uncompressed, {len(df_to_save)} rows) size: {final_size:.2f} MB")

            if final_size <= max_size_mb:
                print(f"  Successfully reduced '{os.path.basename(file_path)}' to {final_size:.2f} MB (within {max_size_mb} MB limit).")
                print(f"  Original rows: {original_row_count}, Reduced rows: {len(df_to_save)}")
                return True, "Reduction successful"
            else:
                if current_sample_ratio <= 0.01: # Don't go below 1% of original rows
                    print(f"  Warning: Could not reduce '{os.path.basename(file_path)}' to {max_size_mb} MB even with {current_sample_ratio*100:.2f}% sampling.")
                    print(f"  Final file is {final_size:.2f} MB. Consider manually reducing data, or using compression on upload.")
                    return False, "Could not meet target size"
                print(f"  Still too large ({final_size:.2f} MB as plain CSV). Reducing sample size further...")
                current_sample_ratio *= 0.8 # Reduce by 20% each time, more aggressive given no compression

        except Exception as e:
            print(f"  Error saving or checking size of '{os.path.basename(file_path)}': {e}")
            return False, f"Error during saving/checking: {e}"

# --- Main script to process all files in 'datasets' folder ---
datasets_folder = "datasets" # Make sure this folder exists in the same directory as this script
max_limit_mb = 24

print(f"Starting CSV file size reduction process for files in '{datasets_folder}' to ensure they are <= {max_limit_mb} MB.")
print("-" * 60)

if not os.path.isdir(datasets_folder):
    print(f"Error: The folder '{datasets_folder}' does not exist in the current directory.")
    print("Please ensure your 'datasets' folder, containing your CSV files, is in the same location as this script.")
else:
    processed_count = 0
    reduced_count = 0
    error_count = 0
    csv_files_found = 0

    for filename in os.listdir(datasets_folder):
        if filename.endswith(".csv"):
            csv_files_found += 1
            file_path = os.path.join(datasets_folder, filename)
            processed_count += 1
            success, message = reduce_csv_size_to_plain_csv(file_path, max_size_mb=max_limit_mb)
            if success and "Reduction successful" in message:
                reduced_count += 1
            elif not success:
                error_count += 1
            print("-" * 60) # Separator for clarity

    if csv_files_found == 0:
        print(f"No CSV files found in the '{datasets_folder}' folder.")
    else:
        print("\n--- Summary ---")
        print(f"Total CSV files found: {csv_files_found}")
        print(f"Total CSV files processed: {processed_count}")
        print(f"Files reduced in size: {reduced_count}")
        print(f"Files with errors: {error_count}")
        print("Processing complete.")