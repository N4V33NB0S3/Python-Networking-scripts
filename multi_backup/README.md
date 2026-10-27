# Multi-vendor Configuration Backup

[← Repository index](../README.md)

`multi_backup.py` connects to each device listed in `devices.txt` over SSH, retrieves its running configuration with a vendor-specific read command, and writes the result to a text file named for the device prompt hostname.

## Requirements

- Python 3
- Netmiko
- SSH reachability from the machine running the script
- A username and password accepted by every listed device

Install Netmiko:

```bash
python -m pip install netmiko
```

The script also uses Python standard-library modules: `getpass` and `concurrent.futures`.

## Files and input format

Place `multi_backup.py` and `devices.txt` in the same working directory, then run the script from that directory. The script opens the literal filename `devices.txt` in the current working directory.

Each non-empty line must contain an IP address or resolvable host and a Netmiko device type separated by a comma:

```text
192.0.2.10,juniper_junos
192.0.2.20,nokia_sros
192.0.2.30,huawei
```

The addresses above are documentation-only examples. Replace them with devices you are authorized to access. Do not add a header row or credentials. Blank lines are skipped. The parser expects exactly two comma-separated fields; malformed lines stop input loading with an error.

## Run

```bash
python multi_backup.py
```

The script prompts for one username and a password. The password prompt uses `getpass`, so the password is not echoed on screen. These same credentials are used for every device in the input list; devices requiring different credentials need separate runs or a code change.

The script submits device jobs to a thread pool with up to five workers. It prints a start message as each device begins and success messages when backups are saved. Press Ctrl+C in the terminal to request interruption. Because the executor context waits for running work to finish as it shuts down, interruption may not stop active SSH operations immediately.

## Supported device types and commands

Use these exact Netmiko device type strings in `devices.txt`:

| Netmiko type | Configuration command | Hostname handling |
| --- | --- | --- |
| `juniper_junos` | `show configuration | display set` | Takes the portion after `@` in Netmiko's base prompt |
| `nokia_sros` | `admin display-config` | Removes `A:` from Netmiko's base prompt |
| `huawei` | `display current-configuration` | Uses Netmiko's base prompt as-is |

These strings and command selections reflect the current script. Device software versions, privilege levels, prompt formats, and command authorization can affect whether a connection or command works. No other vendor type is implemented.

## Output behavior

For each successful device, the script writes the command output as UTF-8 text to `<hostname>.txt` in the current working directory. It overwrites an existing file with the same name. The output does not include a timestamp or separate per-device folder. If two devices produce the same parsed hostname, they target the same filename and one backup may overwrite the other.

Treat the resulting files as sensitive: configurations may expose credentials, keys, addressing, and network design. Save them to an access-controlled location, review them before sharing, and do not commit them to the repository.

## Troubleshooting

- **Cannot open `devices.txt`:** Run from the directory containing the file, or place a copy there. The script does not accept a file path argument.
- **Malformed line / unpacking error:** Ensure every non-empty line contains exactly one comma and both fields, in `host,device_type` order.
- **Authentication failure:** Check the username/password, account status, and device authentication policy. Credentials are shared across all targets in a run.
- **Connection timeout:** Check routing, DNS if using hostnames, SSH service availability, access lists, and the device management address. The script configures connection, banner, and general timeouts of 15, 30, and 30 seconds respectively.
- **Unsupported vendor error:** Use one of `juniper_junos`, `nokia_sros`, or `huawei` exactly.
- **Command rejected or incomplete output:** Confirm the account can run the listed read command and that the device prompt/privilege level is compatible with Netmiko.
- **Backup file missing or unexpectedly named:** The name is derived from Netmiko's base prompt using vendor-specific string handling. Check the prompt format and current directory.
- **Failures are not clearly reported:** The current script does not catch per-device connection or command exceptions. It calls `executor.map` without consuming its results, so worker exceptions may not be printed. Confirm expected backups exist and inspect terminal output. This documentation does not change the script.

## Security and operational notes

- Never place passwords in `devices.txt`, source code, or command-line arguments.
- Use a least-privilege account that can read configuration and connect over SSH.
- Keep the inventory and generated backups out of version control. Consider adding local files such as `devices.txt` and `*.txt` backups to a suitable `.gitignore`.
- Verify the target list before running. This script opens SSH sessions and collects configuration from every listed device.
- Protect and securely dispose of backups according to your organization's retention and data-handling rules.
