import unittest
from app import atbash, substitution, aes_encrypt, aes_decrypt, generate_rsa_pair, rsa_encrypt, rsa_decrypt, hybrid_encrypt, hybrid_decrypt, integrated_encrypt, integrated_decrypt

class CipherTests(unittest.TestCase):
    def test_atbash_round_trip(self):
        text = "Hello, World!"
        self.assertEqual(atbash(atbash(text)), text)

    def test_atbash_known_value(self):
        self.assertEqual(atbash("HELLO"), "SVOOL")

    def test_substitution_round_trip(self):
        text = "Traditional and modern encryption 123!"
        self.assertEqual(substitution(substitution(text), decrypt=True), text)

    def test_aes_round_trip(self):
        text = "AES protects this message."
        result = aes_encrypt(text)
        self.assertEqual(aes_decrypt(result["ciphertext"], result["key"], result["nonce"]), text)

    def test_rsa_round_trip(self):
        public, private = generate_rsa_pair()
        text = "Short RSA message"
        self.assertEqual(rsa_decrypt(rsa_encrypt(text, public), private), text)

    def test_integrated_atbash_aes_rsa_round_trip(self):
        public, private = generate_rsa_pair()
        text = "Traditional and modern encryption work together."
        result = integrated_encrypt(text, "atbash", public)
        self.assertEqual(integrated_decrypt(result["ciphertext"], result["nonce"], result["encrypted_key"], private, "atbash"), text)

    def test_integrated_substitution_aes_rsa_round_trip(self):
        public, private = generate_rsa_pair()
        text = "A second integration test with substitution."
        result = integrated_encrypt(text, "substitution", public)
        self.assertEqual(integrated_decrypt(result["ciphertext"], result["nonce"], result["encrypted_key"], private, "substitution"), text)

    def test_hybrid_round_trip(self):
        public, private = generate_rsa_pair()
        text = "Hybrid encryption supports a longer message than direct RSA."
        result = hybrid_encrypt(text, public)
        self.assertEqual(hybrid_decrypt(result["ciphertext"], result["nonce"], result["encrypted_key"], private), text)

if __name__ == "__main__":
    unittest.main()
