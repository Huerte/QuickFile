<p align="center">
  <img src="https://github.com/user-attachments/assets/71af1eb2-527c-4261-84f8-46e55809a04b" width="900" alt="QuickFile Preview"/>
</p>

<h1 align="center">QuickFile</h1>

<p align="center">
  <img src="https://img.shields.io/badge/version-1.0.0-blue.svg">
  <img src="https://img.shields.io/badge/platform-Python-blueviolet.svg">
  <img src="https://img.shields.io/badge/license-MIT-green.svg">
</p>

<div align="center">
  A lightweight CLI tool to quickly batch-generate files with automatic sequential naming.
</div>

</div>

---

## Features

QuickFile provides a command-line interface designed for rapidly generating placeholder files.  
Built to be fast, simple, and configurable.

- **Automatic Sequential Naming:** Automatically appends increasing numbers (e.g., `file1.txt`, `file2.txt`) to avoid filename collisions.
- **Batch Generation:** Create multiple files of the same extension instantly by specifying a count.
- **Configurable Default Naming:** Easily customize the default prefix name for generated files via command-line configuration.

---

## Installation Guide

Follow these steps to set up QuickFile locally.

### Prerequisites

- **Python 3.8+**

---

### Step 1: Get the Code

```bash
git clone https://github.com/Huerte/QuickFile
cd QuickFile
```

---

### Step 2: Install Package

```bash
pip install -e .
```

To uninstall:
```bash
pip uninstall quickfile
```

---

## Usage

1. **Generate a single file with an extension:**
   ```bash
   mk txt
   ```
   *(Creates `file1.txt`, assuming default prefix `file`)*

2. **Generate multiple files at once:**
   ```bash
   mk txt 5
   ```
   *(Creates `file1.txt`, `file2.txt`, ..., `file5.txt`)*

3. **Generate a file with a specific name:**
   ```bash
   mk my_script.py
   ```
   *(Creates `my_script.py`, or `my_script1.py` if it exists)*

4. **Change the default file prefix:**
   ```bash
   mk config set prefix custom_prefix
   ```

5. **Show other commands:**
   ```bash
   mk --help
   mk --version
   mk config show
   mk config reset
   ```

---

## Project Structure

```
QuickFile/
│
├── pyproject.toml      # Package metadata
├── src/                # Core logic
│   └── quickfile/      # Main package directory
└── README.md
```

---

## Configuration (If Applicable)

QuickFile creates a `config.json` automatically in `~/.quickfile/config.json` when first run or configured.

Edit the configuration using the CLI:

```bash
mk config set prefix your_prefix
```

---

## Contributing

1. Fork the Project  
2. Create a Feature Branch  
3. Commit Changes  
4. Push to Branch  
5. Open Pull Request  

---

## License

Distributed under the MIT License. See `LICENSE` for details.

---

&copy; 2026 [Huerte](https://github.com/Huerte). All Rights Reserved.
