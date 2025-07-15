/**
 * Shift a single letter by `shift` positions, preserving case.
 */
function shiftChar(ch, shift) {
  const isUpper = ch >= "A" && ch <= "Z";
  const base    = isUpper ? 65 : 97;
  const code    = ch.charCodeAt(0);

  // only shift A–Z or a–z
  if ((isUpper && code <= 90) || (!isUpper && code >= 97 && code <= 122)) {
    return String.fromCharCode(((code - base + shift) % 26) + base);
  }
  return ch;
}

/**
 * Core Vigenère transform.
 * direction = +1 for encrypt, -1 for decrypt.
 */
function transform(text, key, direction) {
  let result = "";
  let j = 0;
  const len = key.length;

  for (const ch of text) {
    const kc = key[j % len];
    // compute shift (0–25) from key letter
    const shift =
      ((kc.toLowerCase().charCodeAt(0) - 97) * direction + 26) % 26;
    result += shiftChar(ch, shift);
    // only advance key index on letters
    if (/[A-Za-z]/.test(ch)) j++;
  }
  return result;
}

export const encrypt = (text, key) => transform(text, key, +1);
export const decrypt = (text, key) => transform(text, key, -1);

// Extended test cases
if (import.meta.main) {
  console.log(encrypt("AttackAtDawn!", "KeY"));
  // → "KfAnVfKTvIhq!"
  console.log(decrypt("KfAnVfKTvIhq!", "KeY"));
  // → "AttackAtDawn!"
}