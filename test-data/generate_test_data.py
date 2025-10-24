#!/usr/bin/env python3
"""
Caesar Cipher Test Data Generator

This script generates test data for the Caesar cipher implementation.
It creates multiple test cases with varying shifts and exports the results
in JSON, TXT, and CSV formats.

Usage:
    python generate_test_data.py [--num-cases NUM] [--min-shift MIN] [--max-shift MAX]

Arguments:
    --num-cases NUM    Number of test cases to generate (default: 10)
    --min-shift MIN    Minimum shift value (default: 1)
    --max-shift MAX    Maximum shift value (default: 25)

Examples:
    # Generate 10 test cases with default settings
    python generate_test_data.py
    
    # Generate 20 test cases with shifts between 1 and 10
    python generate_test_data.py --num-cases 20 --min-shift 1 --max-shift 10
    
    # Generate 15 test cases with full shift range
    python generate_test_data.py --num-cases 15

Output:
    - test-data/test_results.json: JSON format with all test cases
    - test-data/test_results.txt: Human-readable text format
    - test-data/test_results.csv: CSV format for spreadsheet analysis

Author: Hacktoberfest Contributor
Issue: #4 - Test Data Generation for Caesar Cipher
"""

import sys
import os
import json
import csv
import argparse
import random
from datetime import datetime

# Add parent directory to path to import caesar cipher
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from ciphers.caesar import encrypt, decrypt


# Sample test phrases with varying complexity
TEST_PHRASES = [
    "Hello, World!",
    "The quick brown fox jumps over the lazy dog.",
    "ATTACK AT DAWN!",
    "Python is awesome!",
    "Cryptography 101",
    "abcdefghijklmnopqrstuvwxyz",
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "Testing 123... Ready?",
    "Hacktoberfest 2024!",
    "Caesar cipher rocks!",
    "Mix3d C4s3 with Numb3rs!",
    "Special characters: @#$%^&*()",
    "Multiple    spaces    here",
    "New\nLine\nTest",
    "Tab\tSeparated\tValues"
]


def generate_test_case(plaintext, shift):
    """
    Generate a single test case with encryption and decryption.
    
    Args:
        plaintext (str): The original text to encrypt
        shift (int): The shift value for Caesar cipher
    
    Returns:
        dict: Test case containing plaintext, shift, encrypted, and decrypted text
    """
    encrypted = encrypt(plaintext, shift)
    decrypted = decrypt(encrypted, shift)
    
    return {
        'plaintext': plaintext,
        'shift': shift,
        'encrypted': encrypted,
        'decrypted': decrypted,
        'matches': plaintext == decrypted  # Verify encryption/decryption works
    }


def generate_test_data(num_cases=10, min_shift=1, max_shift=25):
    """
    Generate multiple test cases with varying shifts.
    
    Args:
        num_cases (int): Number of test cases to generate
        min_shift (int): Minimum shift value
        max_shift (int): Maximum shift value
    
    Returns:
        list: List of test case dictionaries
    """
    test_cases = []
    
    # Ensure we use different phrases and shifts
    for i in range(num_cases):
        plaintext = random.choice(TEST_PHRASES)
        shift = random.randint(min_shift, max_shift)
        test_case = generate_test_case(plaintext, shift)
        test_case['case_number'] = i + 1
        test_cases.append(test_case)
    
    return test_cases


def export_to_json(test_cases, output_dir='test-data'):
    """
    Export test cases to JSON format.
    
    Args:
        test_cases (list): List of test case dictionaries
        output_dir (str): Output directory path
    """
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, 'test_results.json')
    
    output = {
        'metadata': {
            'generated_at': datetime.now().isoformat(),
            'total_cases': len(test_cases),
            'all_passed': all(tc['matches'] for tc in test_cases)
        },
        'test_cases': test_cases
    }
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"✓ JSON output saved to: {filepath}")


def export_to_txt(test_cases, output_dir='test-data'):
    """
    Export test cases to human-readable text format.
    
    Args:
        test_cases (list): List of test case dictionaries
        output_dir (str): Output directory path
    """
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, 'test_results.txt')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write("CAESAR CIPHER TEST RESULTS\n")
        f.write("="*80 + "\n\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Total Test Cases: {len(test_cases)}\n")
        f.write(f"All Tests Passed: {all(tc['matches'] for tc in test_cases)}\n")
        f.write("\n" + "="*80 + "\n\n")
        
        for tc in test_cases:
            f.write(f"Test Case #{tc['case_number']}\n")
            f.write("-"*80 + "\n")
            f.write(f"Plaintext:  {tc['plaintext']}\n")
            f.write(f"Shift:      {tc['shift']}\n")
            f.write(f"Encrypted:  {tc['encrypted']}\n")
            f.write(f"Decrypted:  {tc['decrypted']}\n")
            f.write(f"Match:      {'✓ PASS' if tc['matches'] else '✗ FAIL'}\n")
            f.write("\n")
        
        f.write("="*80 + "\n")
        f.write(f"Summary: {sum(1 for tc in test_cases if tc['matches'])}/{len(test_cases)} tests passed\n")
        f.write("="*80 + "\n")
    
    print(f"✓ TXT output saved to: {filepath}")


def export_to_csv(test_cases, output_dir='test-data'):
    """
    Export test cases to CSV format.
    
    Args:
        test_cases (list): List of test case dictionaries
        output_dir (str): Output directory path
    """
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, 'test_results.csv')
    
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['case_number', 'plaintext', 'shift', 'encrypted', 'decrypted', 'matches']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        writer.writeheader()
        for tc in test_cases:
            writer.writerow(tc)
    
    print(f"✓ CSV output saved to: {filepath}")


def main():
    """
    Main function to parse arguments and generate test data.
    """
    parser = argparse.ArgumentParser(
        description='Generate test data for Caesar cipher implementation',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s
  %(prog)s --num-cases 20
  %(prog)s --num-cases 15 --min-shift 5 --max-shift 20
        """
    )
    
    parser.add_argument(
        '--num-cases',
        type=int,
        default=10,
        help='Number of test cases to generate (default: 10)'
    )
    parser.add_argument(
        '--min-shift',
        type=int,
        default=1,
        help='Minimum shift value (default: 1)'
    )
    parser.add_argument(
        '--max-shift',
        type=int,
        default=25,
        help='Maximum shift value (default: 25)'
    )
    
    args = parser.parse_args()
    
    # Validate arguments
    if args.num_cases < 1:
        print("Error: Number of test cases must be at least 1")
        sys.exit(1)
    
    if args.min_shift < 1 or args.max_shift > 25:
        print("Error: Shift values must be between 1 and 25")
        sys.exit(1)
    
    if args.min_shift > args.max_shift:
        print("Error: Minimum shift cannot be greater than maximum shift")
        sys.exit(1)
    
    print("\n" + "="*80)
    print("CAESAR CIPHER TEST DATA GENERATOR")
    print("="*80)
    print(f"\nGenerating {args.num_cases} test cases...")
    print(f"Shift range: {args.min_shift} to {args.max_shift}\n")
    
    # Generate test data
    test_cases = generate_test_data(args.num_cases, args.min_shift, args.max_shift)
    
    # Export to all formats
    export_to_json(test_cases)
    export_to_txt(test_cases)
    export_to_csv(test_cases)
    
    # Summary
    passed = sum(1 for tc in test_cases if tc['matches'])
    print(f"\n{'='*80}")
    print(f"Test Summary: {passed}/{len(test_cases)} tests passed")
    if passed == len(test_cases):
        print("✓ All tests passed successfully!")
    else:
        print(f"✗ {len(test_cases) - passed} test(s) failed")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
