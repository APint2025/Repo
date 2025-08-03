#!/usr/bin/env python3
"""
Example usage of PDF to CSV Converter components

This script demonstrates how to use the converter components directly
to process text and generate CSV files without needing PDF files.
"""

import pandas as pd
from pdf_to_csv_converter import TextProcessor, CSVConverter


def create_sample_csv_from_key_values():
    """Create a CSV from key-value data."""
    print("Creating CSV from key-value data...")
    
    text = """
Name: Alice Johnson
Age: 28
Department: Marketing
Email: alice.johnson@company.com
Phone: (555) 123-4567
Salary: $65,000
Start Date: 2022-03-15
"""
    
    processor = TextProcessor()
    converter = CSVConverter()
    
    # Extract key-value pairs
    kv_pairs = processor.extract_key_value_pairs(text)
    
    # Create DataFrame
    df = converter.create_dataframe_from_key_values(kv_pairs)
    
    # Save to CSV
    filename = "employee_data.csv"
    converter.save_to_csv(df, filename)
    
    print(f"Created {filename}")
    print(f"Contents:\n{df}")
    return filename


def create_sample_csv_from_tabular_text():
    """Create a CSV from tabular text data."""
    print("\nCreating CSV from tabular text data...")
    
    text = """
Product	Category	Price	Stock	Rating
Laptop	Electronics	$999.99	25	4.5
Mouse	Electronics	$29.99	100	4.2
Desk Chair	Furniture	$199.99	15	4.0
Monitor	Electronics	$299.99	30	4.3
Keyboard	Electronics	$79.99	75	4.1
"""
    
    processor = TextProcessor()
    converter = CSVConverter()
    
    # Split into columns
    rows = processor.split_into_columns(text)
    
    # Use first row as headers
    headers = rows[0] if rows else None
    data_rows = rows[1:] if len(rows) > 1 else []
    
    # Create DataFrame
    df = converter.create_dataframe_from_rows(data_rows, headers)
    
    # Save to CSV
    filename = "inventory_data.csv"
    converter.save_to_csv(df, filename)
    
    print(f"Created {filename}")
    print(f"Contents:\n{df}")
    return filename


def create_sample_csv_from_patterns():
    """Create a CSV from detected patterns."""
    print("\nCreating CSV from detected patterns...")
    
    text = """
Contact List for Project Alpha:

John Smith - john.smith@company.com - (555) 111-2222
Meeting scheduled for 12/15/2023
Budget approved: $25,000

Sarah Davis - sarah.davis@company.com - (555) 333-4444
Deadline: 01/30/2024
Cost estimate: $18,500

Mike Wilson - mike.wilson@company.com - (555) 555-6666
Review date: 11/20/2023
Final amount: $32,750
"""
    
    processor = TextProcessor()
    converter = CSVConverter()
    
    # Detect patterns
    patterns = processor.detect_patterns(text)
    
    # Create DataFrame
    df = converter.create_dataframe_from_patterns(patterns)
    
    # Save to CSV
    filename = "extracted_patterns.csv"
    converter.save_to_csv(df, filename)
    
    print(f"Created {filename}")
    print(f"Contents:\n{df}")
    return filename


def create_sample_csv_from_lines():
    """Create a CSV from lines of text."""
    print("\nCreating CSV from lines of text...")
    
    text = """
Project Milestones:
- Complete requirements analysis
- Design system architecture
- Implement core functionality
- Develop user interface
- Conduct testing phase
- Deploy to production
- Monitor and maintain
"""
    
    processor = TextProcessor()
    converter = CSVConverter()
    
    # Split by lines
    lines = processor.split_by_lines(text)
    
    # Create rows (each line becomes a row)
    rows = [[line] for line in lines]
    
    # Create DataFrame
    df = converter.create_dataframe_from_rows(rows, ['Task'])
    
    # Save to CSV
    filename = "project_tasks.csv"
    converter.save_to_csv(df, filename)
    
    print(f"Created {filename}")
    print(f"Contents:\n{df}")
    return filename


def main():
    """Run all examples."""
    print("PDF to CSV Converter - Example Usage")
    print("=" * 50)
    
    try:
        # Create sample CSV files using different strategies
        files_created = []
        
        files_created.append(create_sample_csv_from_key_values())
        files_created.append(create_sample_csv_from_tabular_text())
        files_created.append(create_sample_csv_from_patterns())
        files_created.append(create_sample_csv_from_lines())
        
        print("\n" + "=" * 50)
        print("Example complete!")
        print(f"Created {len(files_created)} CSV files:")
        for file in files_created:
            print(f"  - {file}")
        
        print("\nThese files demonstrate different text processing strategies.")
        print("You can open them in Excel, Google Sheets, or any CSV viewer.")
        
    except Exception as e:
        print(f"Error during example: {e}")


if __name__ == "__main__":
    main()