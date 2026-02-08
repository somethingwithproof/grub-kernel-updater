# CLAUDE.md

GRUB configuration updater for kernel boot selection.

## Stack
- Python 3.9+

## Lint & Test
```bash
# Syntax check
python3 -m py_compile grub_config_updater.py

# Static analysis
pylint grub_config_updater.py
mypy grub_config_updater.py
```

## Usage
```bash
# Run with caution (requires root)
sudo python3 grub_config_updater.py
```
