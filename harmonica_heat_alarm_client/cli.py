import json
import logging
import os
import time
from argparse import ArgumentParser
from pathlib import Path

from dotenv import dotenv_values
from serial import Serial


def main() -> None:
    parser = ArgumentParser()
    parser.add_argument(
        "--env_file",
        type=Path,
    )
    pre_args, _ = parser.parse_known_args()

    env_vals: dict[str, str | None] = dict(os.environ)

    env_file: Path | None = pre_args.env_file
    if env_file is not None:
        env_vals.update(
            dotenv_values(
                dotenv_path=env_file,
            ),
        )

    logger = logging.getLogger(__name__)
    logging.basicConfig(
        level=logging.INFO,
    )

    parser.add_argument(
        "--port",
        type=str,
        required=env_vals.get("HHAC_PORT") is None,
        default=env_vals.get("HHAC_PORT"),
    )
    parser.add_argument(
        "--baudrate",
        type=int,
        required=env_vals.get("HHAC_BAUDRATE") is None,
        default=env_vals.get("HHAC_BAUDRATE"),
    )
    args = parser.parse_args()

    port: str = args.port
    baudrate: int = args.baudrate

    serial: Serial | None = None
    try:
        serial = Serial(port, baudrate)
        time.sleep(3)  # Wait connection established

        logger.info("send play 1")
        serial.write(
            json.dumps(
                {
                    "type": "play",
                    "count": 1,
                },
            ).encode("ascii")
            + b"\n",
        )
    finally:
        if serial is not None:
            serial.close()
