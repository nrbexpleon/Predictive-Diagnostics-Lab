"""Minimal dependency-free build backend for metadata-only tooling."""

def build_wheel(wheel_directory, config_settings=None, metadata_directory=None):
    raise RuntimeError("Wheel building is intentionally not implemented in the reference lab")

def get_requires_for_build_wheel(config_settings=None):
    return []
