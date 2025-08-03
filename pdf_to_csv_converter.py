#!/usr/bin/env python3
"""
PDF to CSV Converter

This script converts unstructured text from PDF files to structured CSV format.
It supports multiple extraction methods and text processing strategies.
"""

import argparse
import re
import logging
import sys
import os
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
import pandas as pd
import numpy as np

try:
    import PyPDF2
    import pdfplumber
except ImportError as e:
    print(f"Missing required libraries: {e}")
    print("Please install dependencies: pip install -r requirements.txt")
    sys.exit(1)


class PDFTextExtractor:
    """Handles PDF text extraction using multiple methods."""
    
    def __init__(self, pdf_path: str):
        self.pdf_path = Path(pdf_path)
        if not self.pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
    
    def extract_with_pypdf2(self) -> str:
        """Extract text using PyPDF2."""
        text = ""
        try:
            with open(self.pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
        except Exception as e:
            logging.warning(f"PyPDF2 extraction failed: {e}")
        return text
    
    def extract_with_pdfplumber(self) -> str:
        """Extract text using pdfplumber (better for complex layouts)."""
        text = ""
        try:
            with pdfplumber.open(self.pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            logging.warning(f"pdfplumber extraction failed: {e}")
        return text
    
    def extract_tables_with_pdfplumber(self) -> List[List[List[str]]]:
        """Extract tables directly using pdfplumber."""
        tables = []
        try:
            with pdfplumber.open(self.pdf_path) as pdf:
                for page in pdf.pages:
                    page_tables = page.extract_tables()
                    if page_tables:
                        tables.extend(page_tables)
        except Exception as e:
            logging.warning(f"Table extraction failed: {e}")
        return tables
    
    def extract_text(self, method: str = "auto") -> str:
        """Extract text using specified method."""
        if method == "pypdf2":
            return self.extract_with_pypdf2()
        elif method == "pdfplumber":
            return self.extract_with_pdfplumber()
        elif method == "auto":
            # Try pdfplumber first, fallback to PyPDF2
            text = self.extract_with_pdfplumber()
            if not text.strip():
                text = self.extract_with_pypdf2()
            return text
        else:
            raise ValueError(f"Unknown extraction method: {method}")


class TextProcessor:
    """Processes unstructured text into structured data."""
    
    @staticmethod
    def clean_text(text: str) -> str:
        """Clean and normalize text."""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters that might interfere with CSV
        text = re.sub(r'[^\w\s\-\.,;:()\[\]/@#$%&*+=<>?!"\']', '', text)
        return text.strip()
    
    @staticmethod
    def split_by_lines(text: str) -> List[str]:
        """Split text into lines and filter empty ones."""
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        return lines
    
    @staticmethod
    def detect_patterns(text: str) -> Dict[str, List[str]]:
        """Detect common patterns in text (emails, phones, dates, etc.)."""
        patterns = {
            'emails': re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text),
            'phones': re.findall(r'(\+?1[-.\s]?)?(\(?[0-9]{3}\)?[-.\s]?)?[0-9]{3}[-.\s]?[0-9]{4}', text),
            'dates': re.findall(r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b|\b\d{4}[/-]\d{1,2}[/-]\d{1,2}\b', text),
            'numbers': re.findall(r'\b\d+\.?\d*\b', text),
            'currency': re.findall(r'\$\d+\.?\d*|\d+\.?\d*\s*(?:USD|EUR|GBP)', text),
        }
        return patterns
    
    @staticmethod
    def extract_key_value_pairs(text: str) -> List[Tuple[str, str]]:
        """Extract key-value pairs from text."""
        # Pattern for "Key: Value" or "Key = Value"
        kv_pattern = r'([^:\n=]+?)[:=]\s*([^\n]+)'
        matches = re.findall(kv_pattern, text)
        return [(k.strip(), v.strip()) for k, v in matches]
    
    @staticmethod
    def split_into_columns(text: str, delimiters: List[str] = None) -> List[List[str]]:
        """Split text into columns based on delimiters."""
        if delimiters is None:
            delimiters = ['\t', '|', ',', ';', '  ']  # Multiple spaces as delimiter
        
        lines = TextProcessor.split_by_lines(text)
        rows = []
        
        for line in lines:
            # Try different delimiters
            for delimiter in delimiters:
                if delimiter in line:
                    columns = [col.strip() for col in line.split(delimiter)]
                    if len(columns) > 1:  # Only if we actually split something
                        rows.append(columns)
                        break
            else:
                # If no delimiter found, treat as single column
                rows.append([line])
        
        return rows


class CSVConverter:
    """Converts processed text data to CSV format."""
    
    def __init__(self, output_path: str = None):
        self.output_path = output_path
    
    def create_dataframe_from_rows(self, rows: List[List[str]], headers: List[str] = None) -> pd.DataFrame:
        """Create DataFrame from rows of data."""
        if not rows:
            return pd.DataFrame()
        
        # Ensure all rows have the same number of columns
        max_cols = max(len(row) for row in rows)
        normalized_rows = []
        
        for row in rows:
            while len(row) < max_cols:
                row.append('')
            normalized_rows.append(row[:max_cols])
        
        # Create headers if not provided
        if headers is None:
            headers = [f'Column_{i+1}' for i in range(max_cols)]
        
        df = pd.DataFrame(normalized_rows, columns=headers[:max_cols])
        return df
    
    def create_dataframe_from_key_values(self, kv_pairs: List[Tuple[str, str]]) -> pd.DataFrame:
        """Create DataFrame from key-value pairs."""
        if not kv_pairs:
            return pd.DataFrame()
        
        df = pd.DataFrame(kv_pairs, columns=['Key', 'Value'])
        return df
    
    def create_dataframe_from_patterns(self, patterns: Dict[str, List[str]]) -> pd.DataFrame:
        """Create DataFrame from detected patterns."""
        data = []
        for pattern_type, values in patterns.items():
            for value in values:
                data.append({'Type': pattern_type, 'Value': value})
        
        return pd.DataFrame(data)
    
    def save_to_csv(self, df: pd.DataFrame, filename: str = None) -> str:
        """Save DataFrame to CSV file."""
        if filename is None:
            filename = self.output_path or "output.csv"
        
        df.to_csv(filename, index=False, encoding='utf-8')
        return filename


class PDFToCSVConverter:
    """Main converter class that orchestrates the conversion process."""
    
    def __init__(self, pdf_path: str, output_path: str = None, extraction_method: str = "auto"):
        self.pdf_path = pdf_path
        self.output_path = output_path or f"{Path(pdf_path).stem}_converted.csv"
        self.extraction_method = extraction_method
        
        self.extractor = PDFTextExtractor(pdf_path)
        self.processor = TextProcessor()
        self.converter = CSVConverter(output_path)
        
        # Setup logging
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)
    
    def convert_structured_tables(self) -> bool:
        """Try to extract structured tables directly."""
        self.logger.info("Attempting to extract structured tables...")
        tables = self.extractor.extract_tables_with_pdfplumber()
        
        if tables:
            all_rows = []
            for table in tables:
                # Filter out None rows and clean data
                cleaned_table = []
                for row in table:
                    if row and any(cell for cell in row if cell):
                        cleaned_row = [str(cell) if cell else '' for cell in row]
                        cleaned_table.append(cleaned_row)
                
                if cleaned_table:
                    all_rows.extend(cleaned_table)
            
            if all_rows:
                # Use first row as headers if it looks like headers
                headers = None
                data_rows = all_rows
                
                if all_rows and all(isinstance(cell, str) and not cell.replace('.', '').replace(',', '').isdigit() 
                                  for cell in all_rows[0] if cell):
                    headers = all_rows[0]
                    data_rows = all_rows[1:]
                
                df = self.converter.create_dataframe_from_rows(data_rows, headers)
                filename = self.converter.save_to_csv(df, self.output_path)
                self.logger.info(f"Successfully extracted {len(df)} rows to {filename}")
                return True
        
        return False
    
    def convert_unstructured_text(self, strategy: str = "auto") -> str:
        """Convert unstructured text using various strategies."""
        self.logger.info(f"Extracting text using method: {self.extraction_method}")
        text = self.extractor.extract_text(self.extraction_method)
        
        if not text.strip():
            raise ValueError("No text could be extracted from the PDF")
        
        self.logger.info(f"Extracted {len(text)} characters of text")
        
        # Clean the text
        cleaned_text = self.processor.clean_text(text)
        
        if strategy == "lines":
            # Convert each line to a row
            lines = self.processor.split_by_lines(cleaned_text)
            rows = [[line] for line in lines]
            df = self.converter.create_dataframe_from_rows(rows, ['Text'])
            
        elif strategy == "key_value":
            # Extract key-value pairs
            kv_pairs = self.processor.extract_key_value_pairs(cleaned_text)
            df = self.converter.create_dataframe_from_key_values(kv_pairs)
            
        elif strategy == "patterns":
            # Extract patterns (emails, phones, etc.)
            patterns = self.processor.detect_patterns(cleaned_text)
            df = self.converter.create_dataframe_from_patterns(patterns)
            
        elif strategy == "columns":
            # Try to split into columns
            rows = self.processor.split_into_columns(cleaned_text)
            df = self.converter.create_dataframe_from_rows(rows)
            
        elif strategy == "auto":
            # Try different strategies and use the best one
            strategies_to_try = ["columns", "key_value", "patterns", "lines"]
            best_df = None
            best_strategy = None
            best_score = 0
            
            for strat in strategies_to_try:
                try:
                    temp_df = self._try_strategy(cleaned_text, strat)
                    score = self._score_dataframe(temp_df)
                    
                    if score > best_score:
                        best_df = temp_df
                        best_strategy = strat
                        best_score = score
                except Exception as e:
                    self.logger.warning(f"Strategy {strat} failed: {e}")
                    continue
            
            if best_df is not None:
                df = best_df
                self.logger.info(f"Best strategy: {best_strategy} (score: {best_score})")
            else:
                # Fallback to lines strategy
                lines = self.processor.split_by_lines(cleaned_text)
                rows = [[line] for line in lines]
                df = self.converter.create_dataframe_from_rows(rows, ['Text'])
        
        else:
            raise ValueError(f"Unknown strategy: {strategy}")
        
        # Save to CSV
        filename = self.converter.save_to_csv(df, self.output_path)
        self.logger.info(f"Successfully converted to CSV: {filename} ({len(df)} rows)")
        
        return filename
    
    def _try_strategy(self, text: str, strategy: str) -> pd.DataFrame:
        """Try a specific conversion strategy."""
        if strategy == "lines":
            lines = self.processor.split_by_lines(text)
            rows = [[line] for line in lines]
            return self.converter.create_dataframe_from_rows(rows, ['Text'])
            
        elif strategy == "key_value":
            kv_pairs = self.processor.extract_key_value_pairs(text)
            return self.converter.create_dataframe_from_key_values(kv_pairs)
            
        elif strategy == "patterns":
            patterns = self.processor.detect_patterns(text)
            return self.converter.create_dataframe_from_patterns(patterns)
            
        elif strategy == "columns":
            rows = self.processor.split_into_columns(text)
            return self.converter.create_dataframe_from_rows(rows)
            
        else:
            raise ValueError(f"Unknown strategy: {strategy}")
    
    def _score_dataframe(self, df: pd.DataFrame) -> float:
        """Score a DataFrame based on how structured it looks."""
        if df.empty:
            return 0
        
        score = 0
        
        # More columns generally better (up to a point)
        num_cols = len(df.columns)
        score += min(num_cols * 2, 10)
        
        # More rows with data
        non_empty_rows = df.dropna(how='all').shape[0]
        score += non_empty_rows * 0.1
        
        # Prefer DataFrames with consistent column counts
        if num_cols > 1:
            row_lengths = [len([cell for cell in row if pd.notna(cell) and cell != '']) 
                          for _, row in df.iterrows()]
            if row_lengths:
                consistency = 1 - (np.std(row_lengths) / np.mean(row_lengths)) if np.mean(row_lengths) > 0 else 0
                score += consistency * 5
        
        return score
    
    def convert(self, strategy: str = "auto", force_unstructured: bool = False) -> str:
        """Main conversion method."""
        if not force_unstructured:
            # First try to extract structured tables
            if self.convert_structured_tables():
                return self.output_path
        
        # Fall back to unstructured text processing
        return self.convert_unstructured_text(strategy)


def main():
    """Command-line interface for the PDF to CSV converter."""
    parser = argparse.ArgumentParser(description='Convert PDF unstructured text to CSV table')
    parser.add_argument('pdf_path', help='Path to the input PDF file')
    parser.add_argument('-o', '--output', help='Output CSV file path')
    parser.add_argument('-m', '--method', choices=['auto', 'pypdf2', 'pdfplumber'], 
                       default='auto', help='Text extraction method')
    parser.add_argument('-s', '--strategy', choices=['auto', 'lines', 'key_value', 'patterns', 'columns'],
                       default='auto', help='Text processing strategy')
    parser.add_argument('-f', '--force-unstructured', action='store_true',
                       help='Force unstructured text processing (skip table detection)')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose logging')
    
    args = parser.parse_args()
    
    # Setup logging
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    
    try:
        converter = PDFToCSVConverter(args.pdf_path, args.output, args.method)
        output_file = converter.convert(args.strategy, args.force_unstructured)
        print(f"Successfully converted PDF to CSV: {output_file}")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()