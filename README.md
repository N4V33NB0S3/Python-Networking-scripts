# Python Networking Scripts

A growing collection of Python scripts for networking tasks and automation. Each script has its own guide with setup instructions, inputs, supported platforms, and troubleshooting notes.

## Scripts

| Script | Purpose | Guide |
| --- | --- | --- |
| `multi_backup.py` | Collects and saves configuration backups from Juniper Junos, Nokia SR OS, and Huawei devices over SSH using Netmiko. | [Multi-vendor configuration backup guide](multi_backup/README.md) |

## Getting started

1. Review the guide linked above before running a script.
2. Use a supported Python 3 environment and install only the dependencies required by that script.
3. Prepare input files using the format documented in the script guide. Keep credentials and device-specific information out of Git.
4. Run scripts only against devices you are authorized to administer.

## Repository layout

```text
.
├── README.md
├── multi_backup.py
└── multi_backup/
    └── README.md
```

Add future scripts to the table above and give each one a focused guide, for example `<script-name>/README.md`. Keep the global README as a short index; put detailed usage and troubleshooting in each script guide.

## Security

Do not commit passwords, private keys, real device inventories, or configuration backups. Configuration files can contain sensitive information such as credentials, keys, topology, and addressing. Store backups in a protected location and check repository changes before pushing.
