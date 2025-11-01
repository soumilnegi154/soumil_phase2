from custom_encryption import is_prime, generator
 
 
def leak_shared_key(a, b):
    p = 97
    g = 31
    if not is_prime(p) and not is_prime(g):
        print("Enter prime numbers")
        return
    u = generator(g, a, p)
    v = generator(g, b, p)
    key = generator(v, a, p)
    b_key = generator(u, b, p)
    shared_key = None
    if key == b_key:
        shared_key = key
    else:
        print("Invalid key")
        return
 
    return shared_key
 
 
def decrypt(ciphertext, key):
    semi_ciphertext = []
    for num in ciphertext:
        semi_ciphertext.append(chr(round(num / (key * 311))))
    return "".join(semi_ciphertext)
 
 
def dynamic_xor_decrypt(semi_ciphertext, text_key):
    plaintext = ""
    key_length = len(text_key)
    for i, char in enumerate(semi_ciphertext):
        key_char = text_key[i % key_length]
        decrypted_char = chr(ord(char) ^ ord(key_char))
        plaintext += decrypted_char
    return plaintext[::-1]
 
 
if __name__ == "__main__":
    # 0. Take relevant values from `enc_flag` and `custom_encryption.py`
    a = 97
    b = 22
    ciphertext_arr = [151146, 1158786, 1276344, 1360314, 1427490, 1377108, 1074816, 1074816, 386262, 705348, 0, 1393902, 352674, 83970, 1141992, 0, 369468, 1444284, 16794, 1041228, 403056, 453438, 100764, 100764, 285498, 100764, 436644, 856494, 537408, 822906, 436644, 117558, 201528, 285498]

    text_key = "trudeau"
 
    # 1. Get the shared key used in `test`
    shared_key = leak_shared_key(a, b)
 
    # 2. Invert the `encrypt` operation
    semi_ciphertext = decrypt(ciphertext_arr, shared_key)
 
    # 3. Invert the `dynamic_xor_encrypt` operation
    plaintext = dynamic_xor_decrypt(semi_ciphertext, text_key)
 
    # 4. Output the flag
    print(plaintext)
