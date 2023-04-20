import codecs
import requests


def encrypt(plaintext):
    plain_hex = plaintext.encode().hex()
    url = "http://aes.cryptohack.org/ecb_oracle/encrypt/" + plain_hex
    r = requests.get(url)
    r_data = r.json()
    return r_data.get("ciphertext", None)


def pad_flag_guess(guess):
  padding = "A" * (16 - len(guess) % 16)
  padded_guess = padding + guess + padding

  return padded_guess


if __name__ == "__main__":
    letters = "abcdefghijklmnopqrstuvwxyz1234567890_{}"
    flag = ""

    while flag[-1:] != "}":  
        for l in letters:
            flag_guess = flag + l
            padded_guess = pad_flag_guess(flag_guess)
            ciphertext = encrypt(padded_guess)

            guess_output_size = 2 * ((16 - len(flag_guess) % 16) + len(flag_guess))

            encrypted_guess = ciphertext[:guess_output_size]
            encrypted_flag = ciphertext[guess_output_size:guess_output_size*2]
            if encrypted_guess == encrypted_flag:
                flag = flag_guess
                print(l, end="", flush=True)  # print letter just guessed
                break
    print()
