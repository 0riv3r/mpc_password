import json
import sys
import requests
import asyncio

# https://pypi.org/project/nest-asyncio/
# pip install nest-asyncio
import nest_asyncio

from mpyc.runtime import mpc

nest_asyncio.apply() # https://pypi.org/project/nest-asyncio/

secint = mpc.SecInt()

def encode_to_int(text):
    # print(f'Encoding {text}')
    text_bytes = text.encode('utf-8') + b'\x01'  # Pad with 1 to preserve trailing zeroes
    text_int = int.from_bytes(text_bytes, 'little')
    # print(f'encoded text: {text_int}')
    return text_int
    # recoveredbytes = text_int.to_bytes((text_int.bit_length() + 7) // 8, 'little')
    # recoveredstring = recoveredbytes[:-1].decode('utf-8') # Strip pad before decoding
    # print(recoveredstring)


def lambda_handler(event, context):
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """

    res = ''
    stored_password = "e&t.C_^q2RFrP%"
    password = ''
    try:
        password = event['password']
    except KeyError:
        password = event['queryStringParameters']['password']

    encoded_stored_password = encode_to_int(stored_password)
    encoded_password = encode_to_int(password)

    # secret integers
    encrypted_stored_password = secint(encoded_stored_password)
    encrypted_password = secint(encoded_password)

    # print("is {} equal {} ?".format(
    #     mpc.run(mpc.output(encrypted_stored_password)),mpc.run(mpc.output(encrypted_password))))

    if(mpc.run(mpc.output(encrypted_stored_password == encrypted_password))):
        res = "Login succeed"
    else:
        res = "Passwords don't match"


    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": f"login response: {res}",
            # "location": ip.text.replace("\n", "")
        }),
    }
