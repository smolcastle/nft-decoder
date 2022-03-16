# Documentation: https://hub.docker.com/r/tiangolo/uwsgi-nginx-flask/
FROM tiangolo/uwsgi-nginx-flask:python3.8

ENV GETH_ARCHIVE_NODE https://bitter-patient-morning.quiknode.pro/06a726a52ec3fa7434feb1f8eecc52de4d870b3e/
ENV ETHERSCAN_KEY R48UWXJJ48F5VMKI6RXPMAMPMZU9UN9KJ3
ENV UWSGI_INI /app/uwsgi.ini

EXPOSE 80

ADD requirements.txt uwsgi.ini /app/
ADD app /app/app

WORKDIR /app

RUN pip install -r requirements.txt
# Install ethtx dependency from smolcastle github
RUN pip install git+https://github.com/smolcastle/ethtx@bf5d55efe428ab068eeb6b5f1842ff5ea6656d17