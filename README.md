# Acunetix Automation

[![License](https://img.shields.io/github/license/aatif1221/acunetix-automation?style=flat-square)](LICENSE) [![Issues](https://img.shields.io/github/issues/aatif1221/acunetix-automation?style=flat-square)](https://github.com/aatif1221/acunetix-automation/issues)

Python script to automate Acunetix vulnerability scans for bug bounty targets.

## 🚀 Overview

`acunetix.py` is a command-line tool that integrates with Acunetix API to automate vulnerability scanning of multiple targets. It reads URLs from a file and submits them for scanning with configurable scan profiles.

## 💻 Usage

```bash
python3 acunetix.py --file targets.txt --scan-type full
```

### Options

- `--file`: Path to file containing target URLs (one per line)
- `--scan-type`: Scan profile (full, high, weak, crawl, xss, sql)

## ⚙️ Setup

1. Install dependencies:
   ```bash
   pip3 install requests validators
   ```

2. Update `config_data` in `acunetix.py`:
   - Set your Acunetix server URL and port
   - Add your API key

3. Run the script with target URLs

## 📄 License

MIT License. See `LICENSE` for details.
