import json
import sys
import requests
import asyncio

# https://pypi.org/project/nest-asyncio/
# pip install nest-asyncio
import nest_asyncio

from mpyc.runtime import mpc

nest_asyncio.apply() # https://pypi.org/project/nest-asyncio/

stored_password = "e&t.C_^q2RFrP%"

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
    encrypted_password = secint(encoded_password)

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
