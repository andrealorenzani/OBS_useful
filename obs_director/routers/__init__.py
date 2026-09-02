"""Explicit REST/page routers — no generic dynamic dispatcher (Deep Dive Q10).

Each module below owns one coherent slice of the API/page surface. Live
action routes import their payload models and ``apply_*`` functions directly
from the corresponding ``obs_director.effects`` module.
"""
