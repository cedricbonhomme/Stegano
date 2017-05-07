import subprocess
import sys

modules = ["stegano/tools.py",
            "stegano/lsb/lsb.py",
            "stegano/lsbset/lsbset.py",
            "stegano/lsbset/generators.py",
            "stegano/red/red.py",
            "stegano/exifHeader/exifHeader.py",
            "stegano/steganalysis/parity.py",
            "stegano/steganalysis/statistics.py"]

exit_codes = []
for module in modules:
    rc = subprocess.call(["mypy", "--ignore-missing-imports",
                          "--follow-imports", "skip", module])
    exit_codes.append(rc)
sys.exit(max(exit_codes))
