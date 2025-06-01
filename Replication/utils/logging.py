import os

from utils.utils import get_current_time_str, save_file


def save_and_log_result(class_name, parsed_code, output_dir):
    """Handles saving parsed code, logging iteration success, and recording metrics in a CSV file."""

    # Generate a timestamped output file name
    out_file_name = f"{class_name}-{get_current_time_str()}"

    # Save parsed code to output directory
    save_file(parsed_code, output_dir, out_file_name)

    # Construct the absolute output location path
    output_location = os.path.abspath(f"{output_dir}/{out_file_name}.java")

    # Print iteration success message
    return output_location
