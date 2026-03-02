#  cipher-vault - Classic Cipher algorithms

<p align="center">
  <img alt="License"/>
  <img alt="Forks"/>
  <img alt="Stars"/>
  <img alt="Open Issues"/>
  <img alt="Open PRs"/>
</p>

---

**CryptoVault** is an open-source collection of encryption and decryption algorithms in any language.
From classical ciphers like **Caesar**, **Vigenère**, and **Hill**, to modern ones like **AES**, **Base64**, and **XOR** — this repo is a one-stop resource for learning and contributing to cryptography.

Perfect for:
*  Students and educators exploring cryptography fundamentals
*  Beginners looking for open-source contribution ideas
*  Security enthusiasts brushing up on classical techniques

---

##  What's Inside?

```bash
.
├── classical/
│   ├── caesar.py
│   ├── hill.py
# cipher-vault - Classic Cipher algorithms

<p align="center">
  <img alt="License"/>
  <img alt="Forks"/>
  <img alt="Stars"/>
  <img alt="Open Issues"/>
  <img alt="Open PRs"/>
</p>

---

**CryptoVault** is an open-source collection of encryption and decryption algorithms in any language.
From classical ciphers like **Caesar**, **Vigenère**, and **Hill**, to modern ones like **AES**, **Base64**, and **XOR** — this repo is a one-stop resource for learning and contributing to cryptography.

Perfect for:
* Students and educators exploring cryptography fundamentals
* Beginners looking for open-source contribution ideas
* Security enthusiasts brushing up on classical techniques

---

## What's Inside?

```bash
.
├── classical/
│   ├── caesar.py
│   ├── hill.py
│   ├── vigenere.py
│   ├── playfair.py
│   └── affine.py
├── modern/
│   ├── xor_cipher.py
│   ├── aes.py
│   ├── des.py
│   └── base64.py
├── hash/
│   ├── md5.py
│   ├── sha256.py
│   └── hmac.py
├── js-ciphers/
│   └── vigenere.js
└── README.md
```

---

## Getting Started

1. **Fork** this repository
2. Clone it to your local system:
  ```bash
  git clone https://github.com/your-username/cipher-vault.git
  cd cipher-vault
  ```
3. Install dependencies (if required):
  ```bash
  pip install -r requirements.txt
  ```

---

## AES Encryption Module

The AES Encryption Module (`ciphers/aes_encryption.py`) provides secure AES-256 encryption and decryption with support for both text and file encryption.

### Setup Instructions

Install the required dependency:

```bash
pip install pycryptodome
```

### How to Run

#### Interactive Test Mode (No Arguments)

Run the script without arguments to see example usage:

```bash
python ciphers/aes_encryption.py
```

This will demonstrate:
- Key generation
- Text encryption/decryption
- File encryption/decryption
- Automatic verification of results

#### CLI Mode - Text Encryption

Encrypt text with a generated key:

```bash
python ciphers/aes_encryption.py --mode text
```

Encrypt text with a custom key:

```bash
python ciphers/aes_encryption.py --mode text --key "your-base64-encoded-key"
```

#### CLI Mode - File Encryption

Encrypt a .txt file:

```bash
python ciphers/aes_encryption.py --mode file --input input.txt --output encrypted.bin
```

This will output:
- The encrypted file
- The encryption key (Base64)
- The initialization vector/IV (Base64)

**Important**: Save the key and IV - you'll need them to decrypt!

## CLI Mode - File Decryption

Decrypt an encrypted file:

```bash
python ciphers/aes_encryption.py --mode decrypt --input encrypted.bin --output decrypted.txt --key "your-key" --iv "your-iv"
```

### Features

- **Secure Key Generation**: 256-bit (32-byte) keys using cryptographically secure random number generation
- **AES-256 CBC Mode**: Industry-standard encryption with proper padding
- **Text Encryption**: Encrypt and decrypt plain text strings
- **File Encryption**: Encrypt and decrypt .txt files
- **CLI Interface**: Command-line interface using argparse for easy usage
- **Base64 Encoding**: All keys, IVs, and ciphertext are Base64 encoded for easy storage
- **Test Mode**: Built-in examples and verification

### Example Usage

```python
from ciphers.aes_encryption import generate_key, encrypt, decrypt

# Generate a secure key
key = generate_key()

# Encrypt text
plain_text = "Hello, World!"
ciphertext, iv = encrypt(plain_text, key)

# Decrypt text
decrypted = decrypt(ciphertext, key, iv)
print(decrypted)  # Output: Hello, World!
```

---

## Contributing

We welcome contributions! Check out [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Show Your Support

Give us a ⭐ if you found this helpful!

We welcome contributions! Check out [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

##  License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Show Your Support

Give us a star if you found this helpful!
