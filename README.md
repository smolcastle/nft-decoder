## NFT Decoder
-------------
This hosts a flask server through docker container and exposes port 80.

### Requirements
1. GETH archive node. We use our own achive node via erigon.
2. [Etherscan API key](https://etherscan.io/myapikey)
3. Docker
4. Python >= 3.8
5. Access to [smolcastle/ethtx](https://github.com/smolcastle/ethtx) repo.

### For development
```sh
#  Install requirements
> pip install -r requirements.txt

# Install custom ethtx dependency
> pip install git+https://github.com/smolninja/ethtx@master

# copy .env.example to .env and add node URIs
> cp .env.example .env

# run flask app, it will start a flask server on port 5000
> export FLASK_APP=app.main:app
> flask run

# Test GET request. Response should be a json as in outputs folder
> curl http://127.0.0.1:5000/decode/0x9d3cd047d2a76db289ad6c41360cf7d6c6ee8948510f6e93c086d3c5a6fe038e
```

### For production
```sh
# Just run deploy.sh and it will build a docker image. The APIS are exposed at port 80. Inside docker, the flask server is also exposed at port 80
> scripts/deploy.sh

# Test GET request. Response should be a json as in outputs folder
> curl http://127.0.0.1/decode/0x9d3cd047d2a76db289ad6c41360cf7d6c6ee8948510f6e93c086d3c5a6fe038e
```

-------------
### Architecture
1. app folder contains
    * `main.py` defines the flask app
    * `decoders.py` defines the Decoder class
2. scripts folder contains deployment shell scripts
3. Dockerfile uses a `uwsgi-nginx-flask base image` which implements `uwsgi`, `nginx` and `flask`
4. `uwsgi.ini` contains uwsgi configurations