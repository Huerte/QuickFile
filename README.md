<p align="center">
  <img src="https://github.com/user-attachments/assets/71af1eb2-527c-4261-84f8-46e55809a04b" width="900" alt="QuickFile Preview"/>
</p>

<h1 align="center">QuickFile</h1>

<p align="center">
  <img src="https://img.shields.io/badge/version-1.0.0-blue.svg">
  <img src="https://img.shields.io/badge/platform-Python-blueviolet.svg">
  <img src="https://img.shields.io/badge/license-MIT-green.svg">
</p>

<p align="center">
  <b>A lightweight CLI tool to quickly batch-generate files with automatic sequential naming.</b>
</p>

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

- **Python 3.6+**

---

### Step 1: Get the Code

```bash
git clone https://github.com/Huerte/QuickFile
cd QuickFile
```

---

### Step 2: Install Dependencies

_No external dependencies required._

---

### Step 3: Build (If Applicable)

_No build step required._

---

### Step 4: Run / Package

```bash
python src/quick.py <extension_or_filename> [count]
```

---

## Usage

1. **Generate a single file with an extension:**
   ```bash
   python src/quick.py txt
   ```
   *(Creates `file1.txt`, assuming default prefix `file`)*

2. **Generate multiple files at once:**
   ```bash
   python src/quick.py txt 5
   ```
   *(Creates `file1.txt`, `file2.txt`, ..., `file5.txt`)*

3. **Generate a file with a specific name:**
   ```bash
   python src/quick.py my_script.py
   ```
   *(Creates `my_script.py`, or `my_script1.py` if it exists)*

4. **Change the default file prefix:**
   ```bash
   python src/quick.py -s prename=custom_prefix
   ```

---

## Project Structure

```
QuickFile/
│
├── src/                # Core logic
│   ├── quick.py        # Main CLI script
│   └── config.json     # Auto-generated configuration file
└── README.md
```

---

## Configuration (If Applicable)

QuickFile creates a `config.json` automatically when first run to store settings like the default file prefix.

Edit the configuration using the CLI:

```bash
python src/quick.py -s prename=your_prefix
```

Example `config.json` output:

```json
{
  "prename": "your_prefix"
}
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
