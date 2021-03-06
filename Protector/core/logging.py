"""Logging setup"""
# Protector (A telegram bot project)
# Copyright (C) 2021 - Kunaldiwan All rights reserved. Source code available under the AGPL.

# This file is part of Protector.

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

import logging
from datetime import datetime
from os import environ

import colorlog


__all__ = ["setup_log"]


def _level_check(level):
    _str_to_lvl = {
        "CRITICAL": logging.CRITICAL,
        "ERROR": logging.ERROR,
        "WARNING": logging.WARNING,
        "INFO": logging.INFO,
        "DEBUG": logging.DEBUG,
    }
    if level not in _str_to_lvl:
        return logging.INFO
    return _str_to_lvl[level]


def setup_log():
    """Configures logging"""
    log_level = environ.get("LOG_LEVEL", "info")
    level = _level_check(log_level.upper())
    file_path = f"telegram_bot/core/TheProtectorBot-{datetime.now().strftime('%Y-%m-%d')}.log"

    logging.root.setLevel(level)

    # Logging into file
    file_format = "[ %(asctime)s: %(levelname)-9s ] %(name)-31s - %(message)s"
    logfile = logging.FileHandler(file_path)
    formatter = logging.Formatter(file_format, datefmt="%H:%M:%S")
    logfile.setFormatter(formatter)
    logfile.setLevel(level)

    # Logging into stderr with color
    term_format = (
        "  %(bold)s%(asctime)s%(reset)s: "
        "%(log_color)s%(levelname)-9s%(reset)s | %(name)-31s - "
        "%(log_color)s%(message)s%(reset)s"
    )
    stream = logging.StreamHandler()
    formatter = colorlog.ColoredFormatter(term_format, datefmt="%H:%M:%S")
    stream.setLevel(level)
    stream.setFormatter(formatter)

    root = logging.getLogger()
    root.setLevel(level)
    root.addHandler(logfile)
    root.addHandler(stream)

    logging.getLogger("pyrogram").setLevel(logging.WARNING)
