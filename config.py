import os

Class Config
    SESSION_NAME = os.environ.get("SESSION_NAME", ":memory:")
