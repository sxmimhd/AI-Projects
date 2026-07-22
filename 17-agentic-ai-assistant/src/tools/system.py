import os
import platform
import psutil


class SystemTool:

    name = "system"

    description = (
        "Return information about the current computer, "
        "including OS, CPU, RAM, Python version and current directory."
    )

    def execute(self):

        try:

            return {
                "success": True,
                "result": {
                    "os": platform.system(),
                    "os_version": platform.version(),
                    "python": platform.python_version(),
                    "cpu": platform.processor(),
                    "cpu_cores": psutil.cpu_count(logical=True),
                    "ram_gb": round(psutil.virtual_memory().total / (1024**3), 2),
                    "current_directory": os.getcwd(),
                },
                "tool": self.name,
                "error": None,
            }

        except Exception as e:

            return {
                "success": False,
                "result": None,
                "tool": self.name,
                "error": str(e),
            }