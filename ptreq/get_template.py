"""
file-name: get_template.py
file-id: ba570f6b-82d7-4fa0-b42e-e659d99f16e2
project-name: ptreq
project-id: 11320d17-f243-4e2f-a841-e52098b2b439
"""

# [Includes]
from rich import print
from pathlib import Path

# [Functions]

# [Classes]
class GetTemplate:
    def __init__(self, template_path='./ptreq/templates'):
        self.documents = []
        self.modules = []
        if Path(template_path).exists():
            self.modules = [item for item in Path(template_path).iterdir() if item.is_dir()]
        else:
            print(f'Error: {template_path} does not exist.')

    def get_template(self):
        print(f"{self.modules}")

# [Main]
if __name__ == '__main__':
    templates = GetTemplate()
    templates.get_template()