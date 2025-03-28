"""
Main entry point for Autonoma.

This file provides a simple CLI interface to run Autonoma agents.
"""

import argparse
import asyncio
import os
import sys

from app import logger
from app.config import CONFIG

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Autonoma - Autonomous AI Agent Platform")
    parser.add_argument("--config", help="Path to config file")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    return parser.parse_args()

async def main():
    """Main entry point."""
    args = parse_args()

    if args.debug:
        os.environ["AUTONOMA_LOG_LEVEL"] = "DEBUG"

    logger.info("Starting Autonoma")
    logger.info(f"Debug mode: {CONFIG.debug or args.debug}")

    # TODO: Add agent instantiation and task execution here

    logger.info("Autonoma execution completed")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.exception(f"Error occurred: {e}")
        sys.exit(1)
