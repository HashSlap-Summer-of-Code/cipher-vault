function caesarCipher(str, shift) {
    return str.replace(/[a-z]/gi, function(char) {
        const start = char <= 'Z' ? 65 : 97;
        return String.fromCharCode(
            ((char.charCodeAt(0) - start + shift) % 26) + start
        );
    });
}

function encrypt() {
    const text = document.getElementById('plaintext').value;
    const shift = parseInt(document.getElementById('shift').value, 10) || 0;
    const encrypted = caesarCipher(text, shift);
    document.getElementById('result').textContent = encrypted;
} 