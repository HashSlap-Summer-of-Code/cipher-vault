# 🔐 RSA Key Generator (Java)

This Java program generates RSA public/private key pairs, saves them to files, and demonstrates asymmetric encryption/decryption of a short string.

---

## 📂 How It Works

- Generates a 2048-bit RSA key pair using `java.security`
- Saves:
  - `public.key` – Public key in binary format
  - `private.key` – Private key in binary format
- Encrypts a sample string using the public key
- Decrypts the encrypted data using the private key

---

## 🧪 How to Run

### Step 1: Compile the program

```bash
javac java-crypto/RSAKeyGen.java
