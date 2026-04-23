def is_safe_command(cmd):
    blocked = [
        "rm -rf",
        "shutdown",
        "reboot",
        "mkfs",
        ":(){:|:&};:",  # fork bomb
    ]

    return not any(b in cmd.lower() for b in blocked)