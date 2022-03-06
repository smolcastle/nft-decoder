from pathlib import Path
import inspect


ROOT_DIR = Path(
  inspect.getfile(
    inspect.currentframe()
  )
).parent.parent.parent.absolute()
