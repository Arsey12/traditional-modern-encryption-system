# Test Cases

| ID | Test | Expected result |
|---|---|---|
| TC01 | Atbash encrypt `HELLO` | `SVOOL` |
| TC02 | Atbash decrypt `SVOOL` | `HELLO` |
| TC03 | Substitution encrypt then decrypt a sentence | Original sentence is recovered |
| TC04 | AES encrypt then decrypt a message with returned key and nonce | Original message is recovered |
| TC05 | AES decrypt with an incorrect key | Authentication/decryption error |
| TC06 | Generate RSA key pair | Public and private PEM keys are returned |
| TC07 | RSA encrypt and decrypt a short message | Original message is recovered |
| TC08 | Hybrid encrypt and decrypt a longer message | Original message is recovered |
| TC09 | Submit an empty plaintext | Validation error is displayed |
| TC10 | Attempt RSA encryption without a public key | Helpful validation error is displayed |

Run automated unit tests with:

```bash
python -m unittest discover -s tests -v
```
