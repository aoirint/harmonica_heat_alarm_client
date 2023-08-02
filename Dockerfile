# syntax=docker/dockerfile:1.4
FROM python:3.11

RUN <<EOF
    apt-get update
    apt-get install -y \
        gosu
    apt-get clean
    rm -rf /var/lib/apt/lists/*

    groupadd -g 2000 user
    useradd -m -o -u 2000 -g user user
EOF

ADD ./requirements.txt /tmp/
RUN gosu user pip3 install -r /tmp/requirements.txt

ADD ./harmonica_heat_alarm_client /opt/harmonica_heat_alarm_client/scripts/harmonica_heat_alarm_client
ADD ./scripts /opt/harmonica_heat_alarm_client/scripts

ADD ./entrypoint.sh /
ENTRYPOINT [ "/entrypoint.sh" ]

WORKDIR /opt/harmonica_heat_alarm_client
CMD [ "gosu", "user", "python3", "/opt/harmonica_heat_alarm_client/scripts/main.py" ]
