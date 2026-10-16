"""Start unmodified upstream MCP with explicit local-only privacy settings."""

import os

from local_network import install_guard

for variable in (
    "BLENDER_MCP_DISABLE_TELEMETRY", "DISABLE_TELEMETRY",
    "MCP_DISABLE_TELEMETRY", "BLENDERMCP_NO_UPDATE_CHECK", "BLENDER_MCP_SAFE_MODE",
):
    os.environ[variable] = "1"
install_guard()

from blender_mcp.server import main

if __name__ == "__main__":
    main()
