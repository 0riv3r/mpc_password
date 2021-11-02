import json
import sys
import requests
import asyncio
import pickle

# https://pypi.org/project/nest-asyncio/
# pip install nest-asyncio
import nest_asyncio

from mpyc.runtime import mpc

nest_asyncio.apply() # https://pypi.org/project/nest-asyncio/

stored_password = "e&t.C_^q2RFrP%"

# save the pickled encrypted password on the lambda temp file system
# https://docs.aws.amazon.com/lambda/latest/dg/runtimes-context.html
# Each execution environment provides 512 MB of disk space in the /tmp directory.
encrypted_password_file_path = "/tmp/encrypted_password.pkl"


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

async def main(password):
    res = ''
    encoded_stored_password = await encode_to_int(stored_password)
    encoded_password = await encode_to_int(password)

    # secret integers
    encrypted_stored_password = secint(encoded_stored_password)
    encrypted_password_obj = secint(encoded_password)

    # ######## PICKLE  ###########

    # ### with file ###
    # -----------------
    # encrypted_password_file = open(encrypted_password_file_path, 'wb')
    # pickle.dump(encrypted_password_obj, encrypted_password_file)
    # encrypted_password_file.close()

    # encrypted_password_file = open(encrypted_password_file_path, 'rb')
    # encrypted_password = pickle.load(encrypted_password_file)

    # print ("encrypted_password : ", encrypted_password)
    # encrypted_password_file.close()

    # ### No file ###
    # ---------------
    encrypted_password_bytes_sequence = pickle.dumps(encrypted_password_obj)

    encrypted_password = pickle.loads(encrypted_password_bytes_sequence)

    # ############################

    # print("is {} equal {} ?".format(
    #     mpc.run(mpc.output(encrypted_stored_password)),mpc.run(mpc.output(encrypted_password))))

    if(mpc.run(mpc.output(encrypted_stored_password == encrypted_password))):
        res = "Login succeed"
    else:
        res = "Passwords don't match"
        
    return res


def lambda_handler(event, context):
    """Login Lambda function

    Parameters
    ----------
    event: password (string), required

    Returns
    ------
    String: correct or wrong password
    """
    
    try:
        password = event['password']
    except KeyError:
        password = event['queryStringParameters']['password']

    res = asyncio.run(main(password))

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": f"login response: {res}",
            # "location": ip.text.replace("\n", "")
        }),
    }
