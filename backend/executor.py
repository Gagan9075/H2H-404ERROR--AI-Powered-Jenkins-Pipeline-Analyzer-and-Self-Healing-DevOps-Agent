import subprocess
import time
from safety import is_safe_command


def execute_commands(commands, verify_cmd=None, retries=1):
    results = []
    overall_status = "success"

    for cmd in commands:

        # 🔒 Safety Check
        if not is_safe_command(cmd):
            results.append({
                "command": cmd,
                "status": "blocked",
                "error": "Unsafe command"
            })
            overall_status = "failed"
            break

        attempt = 0
        success = False

        while attempt <= retries:
            try:
                process = subprocess.run(
                    cmd,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=30
                )

                step_result = {
                    "command": cmd,
                    "output": process.stdout.strip(),
                    "error": process.stderr.strip(),
                    "status": "success" if process.returncode == 0 else "failed",
                    "attempt": attempt + 1
                }

                results.append(step_result)

                if process.returncode == 0:
                    success = True
                    break
                else:
                    attempt += 1
                    time.sleep(1)

            except Exception as e:
                results.append({
                    "command": cmd,
                    "status": "error",
                    "error": str(e),
                    "attempt": attempt + 1
                })
                attempt += 1
                time.sleep(1)

        # ❌ Stop pipeline if command fails after retries
        if not success:
            overall_status = "failed"
            break

    # 🔍 Verification Phase
    verification = None
    if verify_cmd:
        try:
            v = subprocess.run(
                verify_cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=20
            )

            verification = {
                "command": verify_cmd,
                "output": v.stdout.strip(),
                "error": v.stderr.strip(),
                "status": "success" if v.returncode == 0 else "failed"
            }

            # If verification fails → mark overall failed
            if v.returncode != 0:
                overall_status = "failed"

        except Exception as e:
            verification = {
                "status": "error",
                "error": str(e)
            }
            overall_status = "failed"

    return {
        "status": overall_status,
        "steps": results,
        "verification": verification
    }