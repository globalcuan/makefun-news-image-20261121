import os
import shutil
from pathlib import Path

source = Path(__file__).with_name('entry.png')
os.makedirs('/output', exist_ok=True)
shutil.copyfile(source, '/output/entry.png')
