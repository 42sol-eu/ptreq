"""
file-name: requirement_parser.py
file-id: e6344b6f-1ab2-4463-9d3f-a3bdfaf1bede
project-name: ptreq
project-id: 11320d17-f243-4e2f-a841-e52098b2b439
"""

from rich import print 
from pathlib import Path 

# Setup logging
import logging 
S_LOG_MSG_FORMAT = "%(asctime)s [%(levelname)-5.5s]  %(message)s"
logging.basicConfig(level=logging.DEBUG, format=S_LOG_MSG_FORMAT)
logger = logging.getLogger(__name__)


class RequirementParser:
    """
    Parses requirements from a given file.
    
    """
    def __init__(self, file_path="./requirements", extension=".adoc"):
        if Path(file_path).exists is False:
            logging.error(f"File {file_path} does not exist.")
            raise FileNotFoundError
        self.file_path = file_path
        if extension[0] != '.':
            logging.warning(f"Extension {extension} does not start with a period.\nSet default extension '.adoc' instead.")
            extension = '.adoc'
        self.extension = extension
        # TODO: check for valid extension

    def parse(self):

        # scan folder with subfolders
        for file in Path(self.file_path).glob(f"**/*{self.extension}"):
            print(file)