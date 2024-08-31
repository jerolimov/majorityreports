# see https://github.com/fastapi/fastapi/discussions/7445
# and https://github.com/fastapi/fastapi/discussions/7690

import json
import sys
from main import app

json.dump(app.openapi(), sys.stdout, indent=2)
