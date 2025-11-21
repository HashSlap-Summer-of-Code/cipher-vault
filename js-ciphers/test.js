import { encrypt, decrypt } from './vigenere.js';

// Example usage of the js-ciphers Vigenère implementation
const plain = 'AttackAtDawn!';
const key = 'KeY';

console.log('Plain: ', plain);
const cipher = encrypt(plain, key);
console.log('Encrypted:', cipher);
const back = decrypt(cipher, key);
console.log('Decrypted:', back);

// Run with: node --input-type=module js-ciphers/test.js
