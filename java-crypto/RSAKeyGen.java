
import java.security.*;
import java.security.spec.*;
import java.util.Base64;
import java.io.*;
import javax.crypto.Cipher;

public class RSAKeyGen {

    private static final int KEY_SIZE = 2048;

    public static void main(String[] args) {
        try {
            // Generate RSA Key Pair
            KeyPairGenerator keyGen = KeyPairGenerator.getInstance("RSA");
            keyGen.initialize(KEY_SIZE);
            KeyPair pair = keyGen.generateKeyPair();
            PublicKey publicKey = pair.getPublic();
            PrivateKey privateKey = pair.getPrivate();

            // Save Keys
            saveKeyToFile("public.key", publicKey.getEncoded());
            saveKeyToFile("private.key", privateKey.getEncoded());

            System.out.println("🔐 RSA key pair generated and saved.");

            // Demo: Encrypt and decrypt a short string
            String original = "Hello, RSA!";
            byte[] encrypted = encrypt(original, publicKey);
            String decrypted = decrypt(encrypted, privateKey);

            System.out.println("🔏 Original:  " + original);
            System.out.println("🔒 Encrypted: " + Base64.getEncoder().encodeToString(encrypted));
            System.out.println("🔓 Decrypted: " + decrypted);

        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    private static void saveKeyToFile(String filename, byte[] keyBytes) throws IOException {
        try (FileOutputStream fos = new FileOutputStream(filename)) {
            fos.write(keyBytes);
        }
    }

    private static byte[] encrypt(String data, PublicKey key) throws Exception {
        Cipher cipher = Cipher.getInstance("RSA");
        cipher.init(Cipher.ENCRYPT_MODE, key);
        return cipher.doFinal(data.getBytes());
    }

    private static String decrypt(byte[] data, PrivateKey key) throws Exception {
        Cipher cipher = Cipher.getInstance("RSA");
        cipher.init(Cipher.DECRYPT_MODE, key);
        return new String(cipher.doFinal(data));
    }
}
