#!/usr/bin/env python3
"""
AES Encryption/Decryption Module
Implements secure AES encryption with support for text and file encryption.
"""

import os
import argparse
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import base64


def generate_key():
    """
    Generate a secure 256-bit (32 bytes) AES key.
    
    Returns:
        bytes: A randomly generated 256-bit key
    """
    return get_random_bytes(32)  # 256-bit key


def pad_data(data):
    """
    Pad data to be a multiple of AES block size (16 bytes).
    
    Args:
        data (bytes): Data to be padded
    
    Returns:
        bytes: Padded data
    """
    return pad(data, AES.block_size)


def unpad_data(data):
    """
    Remove padding from decrypted data.
    
    Args:
        data (bytes): Padded data
    
    Returns:
        bytes: Unpadded data
    """
    return unpad(data, AES.block_size)


def encrypt(text, key):
    """
    Encrypt text using AES encryption in CBC mode.
    
    Args:
        text (str): Plain text to encrypt
        key (bytes): 256-bit encryption key
    
    Returns:
        tuple: (encrypted_data_base64, iv_base64) - Base64 encoded ciphertext and IV
    """
    # Convert text to bytes
    text_bytes = text.encode('utf-8')
    
    # Generate a random initialization vector (IV)
    iv = get_random_bytes(AES.block_size)
    
    # Create cipher object
    cipher = AES.new(key, AES.MODE_CBC, iv)
    
    # Pad and encrypt the data
    padded_data = pad_data(text_bytes)
    ciphertext = cipher.encrypt(padded_data)
    
    # Encode to base64 for easy storage/transmission
    ciphertext_b64 = base64.b64encode(ciphertext).decode('utf-8')
    iv_b64 = base64.b64encode(iv).decode('utf-8')
    
    return ciphertext_b64, iv_b64


def decrypt(ciphertext_b64, key, iv_b64):
    """
    Decrypt AES encrypted text.
    
    Args:
        ciphertext_b64 (str): Base64 encoded ciphertext
        key (bytes): 256-bit encryption key
        iv_b64 (str): Base64 encoded initialization vector
    
    Returns:
        str: Decrypted plain text
    """
    # Decode from base64
    ciphertext = base64.b64decode(ciphertext_b64)
    iv = base64.b64decode(iv_b64)
    
    # Create cipher object
    cipher = AES.new(key, AES.MODE_CBC, iv)
    
    # Decrypt and unpad the data
    decrypted_padded = cipher.decrypt(ciphertext)
    decrypted_data = unpad_data(decrypted_padded)
    
    # Convert bytes back to string
    return decrypted_data.decode('utf-8')


def encrypt_file(input_file, output_file, key):
    """
    Encrypt a text file using AES encryption.
    
    Args:
        input_file (str): Path to input file
        output_file (str): Path to output encrypted file
        key (bytes): 256-bit encryption key
    
    Returns:
        str: Base64 encoded IV (needed for decryption)
    """
    # Read the input file
    with open(input_file, 'rb') as f:
        plaintext = f.read()
    
    # Generate a random initialization vector
    iv = get_random_bytes(AES.block_size)
    
    # Create cipher object
    cipher = AES.new(key, AES.MODE_CBC, iv)
    
    # Pad and encrypt the data
    padded_data = pad_data(plaintext)
    ciphertext = cipher.encrypt(padded_data)
    
    # Write encrypted data to output file
    with open(output_file, 'wb') as f:
        f.write(ciphertext)
    
    # Return IV as base64 (needed for decryption)
    return base64.b64encode(iv).decode('utf-8')


def decrypt_file(input_file, output_file, key, iv_b64):
    """
    Decrypt an AES encrypted file.
    
    Args:
        input_file (str): Path to encrypted file
        output_file (str): Path to output decrypted file
        key (bytes): 256-bit encryption key
        iv_b64 (str): Base64 encoded initialization vector
    """
    # Read the encrypted file
    with open(input_file, 'rb') as f:
        ciphertext = f.read()
    
    # Decode IV from base64
    iv = base64.b64decode(iv_b64)
    
    # Create cipher object
    cipher = AES.new(key, AES.MODE_CBC, iv)
    
    # Decrypt and unpad the data
    decrypted_padded = cipher.decrypt(ciphertext)
    decrypted_data = unpad_data(decrypted_padded)
    
    # Write decrypted data to output file
    with open(output_file, 'wb') as f:
        f.write(decrypted_data)


def main():
    """
    Main function with CLI argument parsing.
    """
    parser = argparse.ArgumentParser(
        description='AES Encryption/Decryption Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Text encryption with auto-generated key
  python aes_encryption.py --mode text
  
  # Text encryption with custom key
  python aes_encryption.py --mode text --key "your-base64-key-here"
  
  # File encryption
  python aes_encryption.py --mode file --input input.txt --output encrypted.bin
  
  # File decryption
  python aes_encryption.py --mode decrypt --input encrypted.bin --output decrypted.txt --key "key" --iv "iv"
        """
    )
    
    parser.add_argument(
        '--mode',
        choices=['text', 'file', 'decrypt'],
        default='text',
        help='Operation mode: text encryption, file encryption, or file decryption'
    )
    
    parser.add_argument(
        '--key',
        type=str,
        help='Base64 encoded encryption key (if not provided, a new key will be generated)'
    )
    
    parser.add_argument(
        '--input',
        type=str,
        help='Input file path (for file mode)'
    )
    
    parser.add_argument(
        '--output',
        type=str,
        help='Output file path (for file mode)'
    )
    
    parser.add_argument(
        '--iv',
        type=str,
        help='Base64 encoded IV (required for decryption mode)'
    )
    
    args = parser.parse_args()
    
    # Handle key input
    if args.key:
        try:
            key = base64.b64decode(args.key)
            if len(key) != 32:
                print("Error: Key must be 256 bits (32 bytes)")
                return
        except Exception as e:
            print(f"Error decoding key: {e}")
            return
    else:
        key = generate_key()
        print(f"Generated Key (save this!): {base64.b64encode(key).decode('utf-8')}")
    
    # Execute based on mode
    if args.mode == 'text':
        # Text encryption mode
        text = input("Enter text to encrypt: ")
        ciphertext, iv = encrypt(text, key)
        print(f"\nEncrypted (Base64): {ciphertext}")
        print(f"IV (Base64): {iv}")
        
        # Decrypt to verify
        decrypted = decrypt(ciphertext, key, iv)
        print(f"\nDecrypted (verification): {decrypted}")
        
    elif args.mode == 'file':
        # File encryption mode
        if not args.input or not args.output:
            print("Error: --input and --output are required for file mode")
            return
        
        if not os.path.exists(args.input):
            print(f"Error: Input file '{args.input}' not found")
            return
        
        iv = encrypt_file(args.input, args.output, key)
        print(f"File encrypted successfully!")
        print(f"IV (Base64): {iv}")
        print(f"Encrypted file: {args.output}")
        
    elif args.mode == 'decrypt':
        # File decryption mode
        if not args.input or not args.output or not args.iv:
            print("Error: --input, --output, and --iv are required for decrypt mode")
            return
        
        if not os.path.exists(args.input):
            print(f"Error: Input file '{args.input}' not found")
            return
        
        decrypt_file(args.input, args.output, key, args.iv)
        print(f"File decrypted successfully!")
        print(f"Decrypted file: {args.output}")


if __name__ == "__main__":
    # Check if running with command line arguments
    import sys
    
    if len(sys.argv) > 1:
        # CLI mode
        main()
    else:
        # Interactive test mode
        print("=" * 60)
        print("AES Encryption/Decryption - Test Mode")
        print("=" * 60)
        
        # Generate a secure key
        key = generate_key()
        print(f"\n1. Generated 256-bit Key (Base64): {base64.b64encode(key).decode('utf-8')}")
        
        # Example text encryption
        print("\n2. Text Encryption Example:")
        original_text = "Hello, World! This is a secret message."
        print(f"   Original Text: {original_text}")
        
        encrypted_text, iv = encrypt(original_text, key)
        print(f"   Encrypted (Base64): {encrypted_text}")
        print(f"   IV (Base64): {iv}")
        
        # Decrypt the text
        print("\n3. Text Decryption Example:")
        decrypted_text = decrypt(encrypted_text, key, iv)
        print(f"   Decrypted Text: {decrypted_text}")
        print(f"   Match: {original_text == decrypted_text}")
        
        # File encryption example
        print("\n4. File Encryption Example:")
        test_file = "test_input.txt"
        encrypted_file = "test_encrypted.bin"
        decrypted_file = "test_decrypted.txt"
        
        # Create a test file
        with open(test_file, 'w') as f:
            f.write("This is a test file for AES encryption.\nIt contains multiple lines.\nAES is secure!")
        print(f"   Created test file: {test_file}")
        
        # Encrypt the file
        file_iv = encrypt_file(test_file, encrypted_file, key)
        print(f"   Encrypted to: {encrypted_file}")
        print(f"   File IV (Base64): {file_iv}")
        
        # Decrypt the file
        decrypt_file(encrypted_file, decrypted_file, key, file_iv)
        print(f"   Decrypted to: {decrypted_file}")
        
        # Verify file contents match
        with open(test_file, 'r') as f:
            original_content = f.read()
        with open(decrypted_file, 'r') as f:
            decrypted_content = f.read()
        
        print(f"   File contents match: {original_content == decrypted_content}")
        
        print("\n" + "=" * 60)
        print("All tests completed successfully!")
        print("\nTo use CLI mode, run with arguments. Examples:")
        print("  python aes_encryption.py --mode text")
        print("  python aes_encryption.py --mode file --input file.txt --output encrypted.bin")
        print("  python aes_encryption.py --help")
        print("=" * 60)
