import asyncio
import sys

# https://pypi.org/project/nest-asyncio/
# pip install nest-asyncio
import nest_asyncio

from mpyc.runtime import mpc

nest_asyncio.apply() # https://pypi.org/project/nest-asyncio/

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
    if sys.argv[1:]:
        password = str(sys.argv[1])
        # print(f'Input is: {password}')
    else:
        password = "password123"
        # print(f'Setting input to default: {password}')

    stored_password = "e&t.C_\q2RFrP%"

    encoded_stored_password = await encode_to_int(stored_password)
    encoded_password = await encode_to_int(password)


    # x and y are secret integers
    encrypted_stored_password = secint(encoded_stored_password)
    encrypted_password = secint(encoded_password)

    # print("is {} equal {} ?".format(
    #     mpc.run(mpc.output(encrypted_stored_password)),mpc.run(mpc.output(encrypted_password))))

    if(mpc.run(mpc.output(encrypted_stored_password == encrypted_password))):
        print("Login succeed!")
    else:
        print("Passwords don't match!")


if __name__ == "__main__":
    asyncio.run(main())

# run
# python password.py "e&t.C_\q2RFrP%"
# python password.py "+C%pzA9tM8zJ3r"  


# resources
# ---------

# coroutines:
# https://docs.python.org/3/library/asyncio-task.html#coroutines

# cli args with special-characters
# https://superuser.com/questions/163515/bash-how-to-pass-command-line-arguments-containing-special-characters

# encode a text string into a number
# https://stackoverflow.com/questions/55407713/how-to-encode-a-text-string-into-a-number-in-python

