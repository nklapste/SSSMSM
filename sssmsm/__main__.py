#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""argparse and main entry point script for sssmsm"""

import argparse
import os
import sys
import logging
from logging import getLogger
from logging.handlers import TimedRotatingFileHandler

from cheroot.wsgi import Server as WSGIServer, PathInfoDispatcher

from sssmsm.server import APP

__log__ = getLogger(__name__)

LOG_LEVEL_STRINGS = ["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"]


def log_level(log_level_string: str):
    """argparse type function for determining the specified logging level"""
    if log_level_string not in LOG_LEVEL_STRINGS:
        raise argparse.ArgumentTypeError(
            "invalid choice: {} (choose from {})".format(
                log_level_string,
                LOG_LEVEL_STRINGS
            )
        )
    return getattr(logging, log_level_string, logging.INFO)


def add_log_parser(parser):
    """Add logging options to the argument parser"""
    group = parser.add_argument_group(title="Logging")
    group.add_argument("--log-level", dest="log_level", default="INFO",
                       type=log_level, help="Set the logging output level")
    group.add_argument("--log-dir", dest="log_dir",
                       help="Enable TimeRotatingLogging at the directory "
                            "specified")
    group.add_argument("-v", "--verbose", action="store_true",
                       help="Enable verbose logging")


def init_logging(args, log_file_path):
    """Intake a argparse.parse_args() object and setup python logging"""
    handlers_ = []
    log_format = logging.Formatter(
        fmt="[%(asctime)s] [%(levelname)s] - %(message)s")
    if args.log_dir:
        os.makedirs(args.log_dir, exist_ok=True)
        file_handler = TimedRotatingFileHandler(
            os.path.join(args.log_dir, log_file_path),
            when="d", interval=1, backupCount=7, encoding="UTF-8",
        )
        file_handler.setFormatter(log_format)
        file_handler.setLevel(args.log_level)
        handlers_.append(file_handler)
    if args.verbose:
        stream_handler = logging.StreamHandler(stream=sys.stderr)
        stream_handler.setFormatter(log_format)
        stream_handler.setLevel(args.log_level)
        handlers_.append(stream_handler)

    logging.basicConfig(
        handlers=handlers_,
        level=args.log_level
    )


def get_parser() -> argparse.ArgumentParser:
    """Create and return the argparser for sssmsm"""
    parser = argparse.ArgumentParser(
        description="Start the "
                    "Super Simple Scalable MicroService Manager (SSSMSM)",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    group = parser.add_argument_group(title="Server")
    group.add_argument("-d", "--host", default='localhost',
                       help="Hostname to listen on")
    group.add_argument("-p", "--port", default=8000, type=int,
                       help="Port of the webserver")
    group.add_argument("--debug", action="store_true",
                       help="Run the server in Flask debug mode")

    add_log_parser(parser)

    return parser


def main(argv=sys.argv[1:]) -> int:
    """main entry point for sssmsm"""
    parser = get_parser()
    args = parser.parse_args(argv)
    init_logging(args, "sssmsm.log")

    # Setup and start the flask / cheroot server
    if args.debug:
        APP.run(
            host=args.host,
            port=args.port,
            debug=True
        )
    else:
        path_info_dispatcher = PathInfoDispatcher({'/': APP})
        server = WSGIServer((args.host, args.port), path_info_dispatcher)
        try:
            server.start()
        except KeyboardInterrupt:
            __log__.info("stopping server: KeyboardInterrupt detected")
            server.stop()
            return 0
        except Exception:
            __log__.exception("stopping server: unexpected exception")
            raise

    return 0


if __name__ == "__main__":
    sys.exit(main())
