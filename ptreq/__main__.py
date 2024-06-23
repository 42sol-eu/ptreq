"""
file-name: __main__.py
file-id: edb8b803-2a7a-4ab5-bcf5-e4deff0245f1
project-name: ptreq
project-id: 11320d17-f243-4e2f-a841-e52098b2b439
"""

import click

# Setup logging
import logging
S_LOG_MSG_FORMAT = "%(asctime)s [%(levelname)-5.5s]  %(message)s"
logging.basicConfig(level=logging.DEBUG, format=S_LOG_MSG_FORMAT)
logger = logging.getLogger(__name__)

from .requirement_parser import RequirementParser

@click.command()
@click.option('--config', default='ptreq.yaml', help='Path to the configuration file.')
def cli(config: str):
    """Command line interface for AVAHI Simulator."""
    logger.debug(f"CLI called with config: {config}")
    
    parser = RequirementParser()
    try:
        parser.parse()
    except KeyboardInterrupt:
        logger.info("Parseoperation was interrupted!")


    logger.info("So long, and thanks for all the fish!")
    
if __name__ == "__main__":
    cli()
