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

        
In browser: http://127.0.0.1:3000/signin/?password=%2BC%25pzA9tM8zJ3r  


# Lambda endpoint

Browser:  
https://pngowbrq8k.execute-api.eu-west-1.amazonaws.com/dev/signin/?password=%2BC%25pzA9tM8zJ3r

CLI:  
curl -X GET https://pngowbrq8k.execute-api.eu-west-1.amazonaws.com/dev/signin\?password=123


