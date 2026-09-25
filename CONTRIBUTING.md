# Contributing

Thanks for helping improve VOIDDROP. Keep changes focused and beginner-readable.

1. Create a virtual environment and install with `pip install -e .`.
2. Make changes in `src/voiddrop/` or `web/`.
3. Run `pytest` and check `voiddrop --help` before submitting.
4. Describe user-visible changes and any security implications.

Security-sensitive changes must preserve streaming behavior and ensure every filesystem operation stays inside the configured shared directory. Do not add external upload services, telemetry, credential collection, or arbitrary command execution.
