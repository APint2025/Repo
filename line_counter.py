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
        int: Number of lines in the file
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            return len(lines)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None
    except PermissionError:
        print(f"Error: Permission denied to read file '{filename}'.")
        return None
    except UnicodeDecodeError:
        print(f"Error: Unable to decode file '{filename}' as UTF-8.")
        return None
    except Exception as e:
        print(f"Error: An unexpected error occurred: {e}")
        return None


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
    line_count = count_lines(filename)
    
    if line_count is not None:
        print(f"Number of lines in '{filename}': {line_count}")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()