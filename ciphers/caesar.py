"""
Caesar Cipher Implementation

This script implements the Caesar cipher, a substitution cipher where each letter in the plaintext
is shifted a fixed number of positions down the alphabet.

Supports:
- Encryption and decryption
- Both uppercase and lowercase letters
- Skips non-alphabetic characters

Author: [Your Name]
"""

def encrypt(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            # Shift base depending on case
            base = ord('A') if char.isupper() else ord('a')
            # Shift character and wrap using modulo 26
            shifted = (ord(char) - base + shift) % 26 + base
            result += chr(shifted)
        else:
            result += char  # Keep punctuation and spaces unchanged
    return result


def decrypt(text, shift):
    return encrypt(text, -shift)  # Decryption is reverse of encryption


# 🧪 Test case
if __name__ == "__main__":
    sample = "Hello, World!"
    shift = 3
    encrypted = encrypt(sample, shift)
    decrypted = decrypt(encrypted, shift)

    print(f"Original:   {sample}")
    print(f"Encrypted:  {encrypted}")
    print(f"Decrypted:  {decrypted}")
