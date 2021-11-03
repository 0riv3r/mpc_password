import asyncio
import sys
import  pickle
import codecs
import requests

# https://pypi.org/project/nest-asyncio/
# pip install nest-asyncio
import nest_asyncio

from mpyc.runtime import mpc

nest_asyncio.apply() # https://pypi.org/project/nest-asyncio/

# api-endpoint
# localhost
# URL = "http://127.0.0.1:3000/signin?password="
# lambda endpoint
URL = "https://pngowbrq8k.execute-api.eu-west-1.amazonaws.com/Prod/signin?password="

secint = mpc.SecInt()

async def encode_to_int(text):
    # print(f'Encoding {text}')
    text_bytes = text.encode('utf-8') + b'\x01'  # Pad with 1 to preserve trailing zeroes
    text_int = int.from_bytes(text_bytes, 'little')
    # print(f'encoded text: {text_int}')
    return text_int
    # recoveredbytes = text_int.to_bytes((text_int.bit_length() + 7) // 8, 'little')
    # recoveredstring = recoveredbytes[:-1].decode('utf-8') # Strip pad before decoding
    # print(recoveredstring)


async def main():
    global URL

    if sys.argv[1:]:
        password = str(sys.argv[1])
        # print(f'Input is: {password}')
    else:
        password = "password123"
        # print(f'Setting input to default: {password}')

    # stored_password = "e&t.C_^q2RFrP%"
    # encoded_stored_password = await encode_to_int(stored_password)

    encoded_password = await encode_to_int(password)

    # x and y are secret integers
    # encrypted_stored_password = secint(encoded_stored_password)

    encrypted_password_obj = secint(encoded_password)

    # ######## PICKLE  ###########

    # encrypted_password_file = open("encrypted_password.txt", 'wb')
    # pickle.dump(encrypted_password_obj, encrypted_password_file)
    # encrypted_password_file.close()
    # encrypted_password_file = open("encrypted_password.txt", 'rb')
    # encrypted_password = pickle.load(encrypted_password_file)
    # print ("encrypted_password : ", encrypted_password)
    # encrypted_password_file.close()

    # ### No file ###
    # ---------------

    # print ("encrypted_password_obj : ", encrypted_password_obj)

    encrypted_password_bytes_sequence = codecs.encode(pickle.dumps(encrypted_password_obj), "base64").decode()
    # print ("encrypted_password_bytes_sequence : ", encrypted_password_bytes_sequence)

    # encrypted_password = pickle.loads(codecs.decode(encrypted_password_bytes_sequence.encode(), "base64"))
    # print ("encrypted_password : ", encrypted_password)

    # ############################

    ### Send http request
    ### =================

    # URL = "https://pngowbrq8k.execute-api.eu-west-1.amazonaws.com/Prod/signin/?password=gASVmAAAAAAAAACMDW1weWMuc2VjdHlwZXOUjAhTZWNJbnQzMpSTlCmBlE59lIwFc2hhcmWUjA5tcHljLmZpbmZpZWxkc5SMGlByaW1lRmllbGRFbGVtZW50LmNyZWF0ZUdGlJOUKIoJYwAAAAAAAIAASwBLAooJYgAAAAAAAIAAdJRSlE59lIwFdmFsdWWUigi5kxDMCoN7cHOGlGJzhpRiLg=="

    # there are new-line chars inside the base64 string which need to be removed for the json parser to work
    PARAMS = {'password':encrypted_password_bytes_sequence.replace("\n", "")}
 
    res = requests.get(url = URL, params = PARAMS)
    #print(f"res: {res.text}")
    print(res.json())


if __name__ == "__main__":
    asyncio.run(main())

# run
# python password.py "e&t.C_^q2RFrP%"  --> url encoding: e%26t.C_%5Eq2RFrP%25
# python password.py "+C%pzA9tM8zJ3r"  --> url encoding: %2BC%25pzA9tM8zJ3r


# resources
# ---------

# coroutines:
# https://docs.python.org/3/library/asyncio-task.html#coroutines

# cli args with special-characters
# https://superuser.com/questions/163515/bash-how-to-pass-command-line-arguments-containing-special-characters

# encode a text string into a number
# https://stackoverflow.com/questions/55407713/how-to-encode-a-text-string-into-a-number-in-python

