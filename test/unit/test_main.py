# -*- coding: utf-8 -*-

"""pytests for :mod:`ghast.__main__`"""

import argparse
import logging

import pytest

from ghast.__main__ import get_parser, log_level, main


def test_get_parser():
    parser = get_parser()
    assert isinstance(parser, argparse.ArgumentParser)


@pytest.mark.parametrize(
    "log_level_string, expected",
    [
        ("DEBUG", logging.DEBUG),
        ("INFO", logging.INFO),
        ("WARNING", logging.WARNING),
        ("ERROR", logging.ERROR),
        ("CRITICAL", logging.CRITICAL),
    ]
)
def test_log_level(log_level_string, expected):
    assert log_level(log_level_string) == expected


def test_log_level_invalid():
    with pytest.raises(argparse.ArgumentTypeError):
        log_level("INVALID_LOG_LEVEL")


def test_main_invalid_url_arg():
    with pytest.raises(ValueError):
        main(["INVALID_URL"])
