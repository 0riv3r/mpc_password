# mpc_password

# Setup

Download the files from: https://pypi.org/project/mpyc/#files  


        conda create --name mpc
        conda activate mpc
        conda install gmpy2
        conda install numpy pandas matplotlib
        conda install -c conda-forge lifelines
        conda list scikit-learn
        conda install -c anaconda scikit-learn
        conda install -c anaconda requests
        cd mpyc-0.7
        python setup.py install
        cd ..

        # add the following to the python env
        pip install nest-asyncio


# Sanity

        Python

        >>> from mpyc.runtime import mpc
        >>> secint = mpc.SecInt()
        >>> secint.bit_length
        32 # the bit length of the secret integer


        >>> x = secint(3)
        >>> y = secint(5)
        # x and y are secret integers
        >>> x
        >>> y
        >>> mpc.output(x)
        >>> z = mpc.output(x * y)
        >>> z
        # at this point z is a coroutine object, 
        # which means that we were greedily and we've returned immediately, 
        # but nothing happened because we did not run this z coroutine object yet
        >>> mpc.run(z)
        >>> mpc.run(mpc.output(x+y))

        >>> x = mpc.random_bit(secint)
        >>> print(mpc.run(mpc.output(x)))
        0
        >>> x = mpc.random_bit(secint)
        >>> print(mpc.run(mpc.output(x)))
        1


# Demos

https://mpyc.readthedocs.io/en/latest/demos.html#helloworld-py  

        cd /workspace/mpc
        conda activate mpc
        git clone https://github.com/lschoe/mpyc.git
        cd mpyc/demos
        python helloworld.py -M 5


# Lambda

according to: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-getting-started-hello-world.html  


                sam build
                sam local invoke "LoginFunction" -e events/event.json 

                (sam deploy --guided)
                sam deploy

# Run options

### Passwords  
"e&t.C_^q2RFrP%"  --> url encoding: e%26t.C_%5Eq2RFrP%25  
"+C%pzA9tM8zJ3r"  --> url encoding: %2BC%25pzA9tM8zJ3r  


#### CLI
# python password.py "e&t.C_^q2RFrP%"
# python password.py "+C%pzA9tM8zJ3r"


#### Invoke the lambda function directly (data parameters in event.json file):

                sam local invoke "LoginFunction" -e events/event.json

#### Local server

Launch one Terminal:  

                sam local start-api

In a second Terminal, run:

                curl http://127.0.0.1:3000/signin\?password=e%26t.C_%5Eq2RFrP%25

                curl http://127.0.0.1:3000/signin\?password\=gASVmAAAAAAAAACMDW1weWMuc2VjdHlwZXOUjAhTZWNJbnQzMpSTlCmBlE59lIwFc2hhcmWUjA5tcHljLmZpbmZpZWxkc5SMGlByaW1lRmllbGRFbGVtZW50LmNyZWF0ZUdGlJOUKIoJYwAAAAAAAIAASwBLAooJYgAAAAAAAIAAdJRSlE59lIwFdmFsdWWUigi5kxDMCoN7cHOGlGJzhpRiLg==
                {"message": "login response: Login succeed"}%             

        
In browser: http://127.0.0.1:3000/signin/?password=%2BC%25pzA9tM8zJ3r  


# Lambda endpoint

Browser:  
https://pngowbrq8k.execute-api.eu-west-1.amazonaws.com/dev/signin/?password=%2BC%25pzA9tM8zJ3r

CLI:  
curl -X GET https://pngowbrq8k.execute-api.eu-west-1.amazonaws.com/dev/signin\?password=123



### pickle/unpickle output:  
                ❯ python password.py "e&t.C_^q2RFrP%"
                encrypted_password_obj :  <mpyc.sectypes.SecInt32 object at 0x10db60970>
                encrypted_password_bytes_sequence :  b'\x80\x04\x95\x98\x00\x00\x00\x00\x00\x00\x00\x8c\rmpyc.sectypes\x94\x8c\x08SecInt32\x94\x93\x94)\x81\x94N}\x94\x8c\x05share\x94\x8c\x0empyc.finfields\x94\x8c\x1aPrimeFieldElement.createGF\x94\x93\x94(\x8a\tc\x00\x00\x00\x00\x00\x00\x80\x00K\x00K\x02\x8a\tb\x00\x00\x00\x00\x00\x00\x80\x00t\x94R\x94N}\x94\x8c\x05value\x94\x8a\x08\xb9\x93\x10\xcc\n\x83{ps\x86\x94bs\x86\x94b.'
                encrypted_password :  <mpyc.sectypes.SecInt32 object at 0x10db605e0>
                Login succeed!