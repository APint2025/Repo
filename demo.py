#!/usr/bin/env python3
"""
Demo script for PDF to CSV Converter

This script demonstrates how to use the PDF to CSV converter programmatically
and shows examples of different processing strategies.
"""

import os
import tempfile
from pathlib import Path
from pdf_to_csv_converter import PDFToCSVConverter, TextProcessor


def create_sample_text_data():
    """Create sample text data for demonstration."""
    sample_texts = {
        "key_value_sample": """
Name: John Smith
Email: john.smith@email.com
Phone: (555) 123-4567
Address: 123 Main Street, Anytown, ST 12345
Department: Engineering
Employee ID: EMP001
Start Date: 2023-01-15
Salary: $75,000
""",
        
        "tabular_sample": """
Product	Category	Price	Stock
Laptop	Electronics	$999.99	25
Mouse	Electronics	$29.99	100
Desk Chair	Furniture	$199.99	15
Monitor	Electronics	$299.99	30
Keyboard	Electronics	$79.99	75
""",
        
        "mixed_patterns_sample": """
Contact Information Directory

John Doe - john.doe@company.com - (555) 111-2222
Meeting: 12/15/2023 at 2:00 PM
Budget: $15,000 USD

Jane Smith - jane.smith@company.com - (555) 333-4444  
Project deadline: 01/30/2024
Estimated cost: $25,500

Bob Johnson - bob.johnson@company.com - (555) 555-6666
Review date: 11/20/2023
Amount: $8,750 EUR
""",
        
        "list_sample": """
Project Tasks:
- Design user interface mockups
- Implement authentication system
- Create database schema  
- Write API documentation
- Set up testing framework
- Deploy to staging environment
- Conduct user acceptance testing
- Prepare production deployment
"""
    }
    return sample_texts


def demonstrate_text_processing():
    """Demonstrate text processing capabilities."""
    print("="*60)
    print("PDF to CSV Converter - Text Processing Demo")
    print("="*60)
    
    samples = create_sample_text_data()
    processor = TextProcessor()
    
    for sample_name, text in samples.items():
        print(f"\n--- {sample_name.replace('_', ' ').title()} ---")
        print("Original text:")
        print(text[:200] + "..." if len(text) > 200 else text)
        print()
        
        # Demonstrate different processing methods
        if "key_value" in sample_name:
            print("Key-Value pairs extracted:")
            kv_pairs = processor.extract_key_value_pairs(text)
            for key, value in kv_pairs:
                print(f"  {key}: {value}")
        
        elif "tabular" in sample_name:
            print("Column structure detected:")
            rows = processor.split_into_columns(text)
            for i, row in enumerate(rows[:3]):  # Show first 3 rows
                print(f"  Row {i+1}: {row}")
        
        elif "patterns" in sample_name:
            print("Patterns detected:")
            patterns = processor.detect_patterns(text)
            for pattern_type, values in patterns.items():
                if values:
                    print(f"  {pattern_type}: {values}")
        
        elif "list" in sample_name:
            print("Lines extracted:")
            lines = processor.split_by_lines(text)
            for i, line in enumerate(lines[:5]):  # Show first 5 lines
                print(f"  {i+1}: {line}")
        
        print("-" * 40)


def demonstrate_api_usage():
    """Demonstrate programmatic API usage."""
    print("\n" + "="*60)
    print("API Usage Examples")
    print("="*60)
    
    # Note: This would normally work with actual PDF files
    print("\n1. Basic usage:")
    print("   converter = PDFToCSVConverter('input.pdf', 'output.csv')")
    print("   output_file = converter.convert()")
    
    print("\n2. With specific extraction method:")
    print("   converter = PDFToCSVConverter('input.pdf', extraction_method='pdfplumber')")
    print("   output_file = converter.convert(strategy='key_value')")
    
    print("\n3. Force unstructured processing:")
    print("   output_file = converter.convert(strategy='columns', force_unstructured=True)")
    
    print("\n4. Programmatic text processing:")
    processor = TextProcessor()
    sample_text = "Name: John Doe\nEmail: john@example.com\nPhone: 555-1234"
    
    kv_pairs = processor.extract_key_value_pairs(sample_text)
    print(f"   Sample input: {repr(sample_text)}")
    print(f"   Extracted pairs: {kv_pairs}")


def demonstrate_strategy_comparison():
    """Demonstrate how different strategies work on the same text."""
    print("\n" + "="*60)
    print("Strategy Comparison")
    print("="*60)
    
    sample_text = """
Product: Laptop Computer
Model: XPS-15
Price: $1,299.99
Quantity: 5
Category: Electronics
"""
    
    processor = TextProcessor()
    print(f"Sample text:\n{sample_text}")
    print("\nResults by strategy:")
    
    # Lines strategy
    lines = processor.split_by_lines(sample_text)
    print(f"\n1. Lines strategy ({len(lines)} lines):")
    for i, line in enumerate(lines, 1):
        print(f"   {i}: {line}")
    
    # Key-Value strategy
    kv_pairs = processor.extract_key_value_pairs(sample_text)
    print(f"\n2. Key-Value strategy ({len(kv_pairs)} pairs):")
    for key, value in kv_pairs:
        print(f"   {key} → {value}")
    
    # Patterns strategy
    patterns = processor.detect_patterns(sample_text)
    print(f"\n3. Patterns strategy:")
    for pattern_type, values in patterns.items():
        if values:
            print(f"   {pattern_type}: {values}")
    
    # Columns strategy  
    rows = processor.split_into_columns(sample_text)
    print(f"\n4. Columns strategy ({len(rows)} rows):")
    for i, row in enumerate(rows, 1):
        print(f"   Row {i}: {row}")


def main():
    """Run the complete demonstration."""
    print("Welcome to the PDF to CSV Converter Demo!")
    print("This demo shows the text processing capabilities without requiring PDF files.")
    
    try:
        demonstrate_text_processing()
        demonstrate_strategy_comparison()
        demonstrate_api_usage()
        
        print("\n" + "="*60)
        print("Demo Complete!")
        print("="*60)
        print("\nTo use with actual PDF files, try:")
        print("  python pdf_to_csv_converter.py your_file.pdf")
        print("  python pdf_to_csv_converter.py your_file.pdf -s key_value -v")
        print("\nFor more options, see:")
        print("  python pdf_to_csv_converter.py --help")
        
    except Exception as e:
        print(f"Demo error: {e}")


if __name__ == "__main__":
    main()