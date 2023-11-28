import random
import math

LENGTH = 128
CHUNK = LENGTH * 2


def rsa_encrypt(message, e, n):
    m_length = len(message)
    ciphertext = ''
    ascii_message = [0 for i in range(0, m_length)]

    for i in range(0, m_length):
        ascii_message[i] = ord(message[i])

    word_count = 1
    phrase = ascii_message[0]
    for c in range(1, m_length):
        phrase = 256 * phrase + ascii_message[c]

        if c == word_count * 2 - 1 or c == m_length - 1:
            encrypted_string = str(pow(phrase, e, n))
            while len(encrypted_string) < CHUNK:
                encrypted_string = str("0") + encrypted_string
            ciphertext += encrypted_string
            encrypted_string = ''
            word_count += 1
            phrase = 0

    return ciphertext


def rsa_decrypt(message, d, n):
    m_length = len(message)
    encoded_message = [0 for i in range(0, 16384)]
    encoded_message_string = ''
    char_num = 0
    phrase_num = 1

    while char_num < m_length:
        encoded_message_string += message[char_num]
        if char_num == CHUNK * phrase_num - 1:
            encoded_message[phrase_num] = int(encoded_message_string)
            encoded_message_string = ''
            phrase_num += 1
        char_num += 1
    result = ''
    reversed_decoded_message = ['' for j in range(0, phrase_num)]
    for i in range(0, phrase_num):
        decrypted_base128 = pow(encoded_message[i], int(d), int(n))
        decoded_message = ''
        while decrypted_base128 != 0:
            temp = int(decrypted_base128 % 256)
            decrypted_base128 = decrypted_base128 / 256
            decoded_ascii_char = chr(temp)
            decoded_message += decoded_ascii_char
        reversed_decoded_message[i] += decoded_message[::-1]
    for k in range(0, phrase_num):
        result += reversed_decoded_message[k]

    return result


def fermat(prime_length):
    if prime_length <= 0:
        return 0
    N = random.randrange(pow(10, prime_length - 1), pow(10, prime_length))
    if (N % 2) == 0:
        N = N + 1
    correct = 0
    for i in range(0, 20):
        test_num = random.randint(1, N - 1)
        if pow(test_num, N - 1, N) == 1:
            correct = correct + 1

    if correct >= 19:
        return N
    else:
        return 0


def keygen(length):
    p = 0
    q = 0
    public_key = []
    private_key = []
    gcd = 0

    while p == 0:
        p = fermat(length)
    while q == 0:
        q = fermat(length)

    phi = int((p - 1) * (q - 1))
    n = int(p * q)
    while gcd != 1:
        e = int(random.randrange(1, phi))
        gcd = math.gcd(phi, e)
    d = int(pow(e, -1, phi))

    private_key = [d, n]
    public_key = [e, n]
    return private_key, public_key


def main():
    private_key, public_key = keygen(LENGTH)
    message = 'Hello darkness, my old friend.'

    print()
    print("message: " + message)
    print()
    print("encrypting...")
    print()
    ct = rsa_encrypt(message, public_key[0], public_key[1])
    print("ciphertext: " + ct)
    print()
    print("decrypting...")
    print()
    pt = rsa_decrypt(ct, private_key[0], private_key[1])
    print("plaintext: " + pt)
    print()
    print("private: " + str(private_key[0]))
    print("public:  " + str(public_key[0]))


if __name__ == '__main__':
    main()
