#!/usr/bin/env python3
"""
A program that reads a text file and outputs the number of lines in that file.
"""

import sys
import os


def count_lines(filename):
    """
    Count the number of lines in a text file.
    
    Args:
        filename (str): Path to the text file
        
    Returns:
        tuple: (number of lines, list of unparseable lines info) or (None, None) on error
    """
    try:
        with open(filename, 'rb') as file:  # Open in binary mode first
            lines = file.readlines()
            
        parsed_lines = 0
        unparseable_lines = []
        
        for line_num, line_bytes in enumerate(lines, 1):
            try:
                # Try to decode each line
                line_text = line_bytes.decode('utf-8')
                parsed_lines += 1
            except UnicodeDecodeError as e:
                # Record unparseable line information
                unparseable_lines.append({
                    'line_number': line_num,
                    'raw_bytes': line_bytes[:50],  # First 50 bytes for display
                    'error': str(e)
                })
        
        return parsed_lines + len(unparseable_lines), unparseable_lines
        
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None, None
    except PermissionError:
        print(f"Error: Permission denied to read file '{filename}'.")
        return None, None
    except Exception as e:
        print(f"Error: An unexpected error occurred: {e}")
        return None, None


def main():
    """Main function to handle command line arguments and execute the program."""
    if len(sys.argv) != 2:
        print("Usage: python line_counter.py <filename>")
        print("Example: python line_counter.py sample.txt")
        sys.exit(1)
    
    filename = sys.argv[1]
    
    # Check if file exists
    if not os.path.exists(filename):
        print(f"Error: File '{filename}' does not exist.")
        sys.exit(1)
    
    # Count lines
    line_count, unparseable_lines = count_lines(filename)
    
    if line_count is not None:
        print(f"Number of lines in '{filename}': {line_count}")
        
        # Print information about unparseable lines
        if unparseable_lines:
            print(f"\nFound {len(unparseable_lines)} line(s) that could not be parsed:")
            print("-" * 60)
            for line_info in unparseable_lines:
                print(f"Line {line_info['line_number']}:")
                print(f"  Raw bytes (first 50): {line_info['raw_bytes']}")
                print(f"  Error: {line_info['error']}")
                print()
        else:
            print("All lines were successfully parsed.")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()