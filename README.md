# 🔐 cipher-vault - Classic Cipher algorithms

<p align="center">
  <img alt="License" src="https://img.shields.io/badge/license-MIT-blue.svg">
  <img alt="Forks" src="https://img.shields.io/github/forks/HashSlap-Summer-of-Code/cipher-vault?style=social">
  <img alt="Stars" src="https://img.shields.io/github/stars/HashSlap-Summer-of-Code/cipher-vault?style=social">
  <img alt="Open Issues" src="https://img.shields.io/github/issues/HashSlap-Summer-of-Code/cipher-vault">
  <img alt="Open PRs" src="https://img.shields.io/github/issues-pr/HashSlap-Summer-of-Code/cipher-vault">
</p>

---

**CryptoVault** is an open-source collection of encryption and decryption algorithms in any language.
From classical ciphers like **Caesar**, **Vigenère**, and **Hill**, to modern ones like **AES**, **Base64**, and **XOR** — this repo is a one-stop resource for learning and contributing to cryptography.

Perfect for:
* 🧠 Students and educators exploring cryptography fundamentals
* 🧑‍💻 Beginners looking for open-source contribution ideas
* 🔐 Security enthusiasts brushing up on classical techniques

---

## 🧰 What's Inside?

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

## 🚀 Getting Started

1. **Fork** this repository 🍴
2. Clone it to your local system:
   ```bash
   git clone https://github.com/your-username/cryptovault.git
   cd cryptovault
   ```
3. Explore the folders and run any cipher script!
4. Want to contribute? Check out [Issues](https://github.com/HashSlap-Summer-of-Code/cryptovault/issues)

---

## 🤝 Contribution Guidelines

* 📂 Place your cipher in the correct folder (`classical/`, `modern/`, or `hash/`)
* 📝 Add a short description as comments in your script
* ✅ Make sure your code is clean and well-documented
* 🧪 Include a test input/output in your script if possible
* 💬 Open an issue if you're unsure — we're happy to help!

---

## 📚 Learning Resources

* **[CryptoBasics.java](docs/CryptoBasics.java)**: Comprehensive educational documentation covering fundamental cryptography concepts including:
  - Symmetric vs Asymmetric encryption
  - Substitution vs Transposition ciphers
  - One-time pads and their theoretical security
  - Stream vs Block ciphers with examples
  - Practical demonstrations and cryptography glossary

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).

---

## 🌟 Made with 💻 & 🔐 by

<p align="center">
  <b>HashSlap Summer of Code (HSSoC)</b> 🚀
  <br>
  <a href="https://github.com/HashSlap-Summer-of-Code" target="_blank">
    https://github.com/HashSlap-Summer-of-Code
  </a>
</p>

## 🔠 Ciphers

- **[Caesar Cipher](ciphers/caesar.py)**: A simple classical cipher that shifts letters by a fixed number in the alphabet.
- **[Vigenère Cipher](js-ciphers/vigenere.js)**:  A key‑based polyalphabetic substitution cipher; exposes encrypt(text, key) and decrypt(cipher, key).

## Caesar Cipher Visualizer

Test the Caesar cipher in your browser: [Open Visualizer](web/index.html)
This tool lets you enter plaintext and a shift value to see the encrypted result instantly.

---
