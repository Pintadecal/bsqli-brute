# bsqli-brute (beta)
bsqli-brute is a Python-based tool designed for automating time-based blind SQL Injection (SQLi) attacks. This tool is designed to help penetration testers and security researchers extract sensitive information such as database names, table names, and column data from vulnerable web applications using time-delay techniques. With this tool, you can target URLs vulnerable to SQL injection and retrieve data by leveraging time-based blind SQL injection methods.

## Features

Time-based Blind SQL Injection: Automates the process of exploiting time-based blind SQLi vulnerabilities.
Extract Database Names: Retrieve the name of the active database.
Extract Table Names: Retrieve the list of tables from a specific database.
Extract Column Names: Retrieve column names from specific tables in a database.
Data Dumping: Dump data from selected columns for deeper insights.
Logging: Save results to specified files for future analysis.
Custom Delay: Control the delay time to fine-tune the SQLi process.

## Usage

```bash
python3 bsqli-brute.py <URL> <DELAY> [options]
```

## Arguments

<URL>: The target URL vulnerable to SQL injection.
<DELAY>: Delay time (in seconds) for the time-based SQL injection.
--db: Extract the database name.
-D, --database: Specify the target database.
--table: Extract the list of tables.
-T, --table_name: Specify the table name to target for column extraction.
--column: Extract columns from the specified table.
-C, --columns: Specify the columns to dump data from (comma-separated).
--dump: Dump data from selected columns.
--output-dir: Specify the output directory to save logs.

## Example

Extract table names from a specific database:
```bash
python3 bsqli-brute.py https://example.com/vuln.php?cat= 2 -D target_db --table
```

Dump data from specific columns:
```bash
python3 bsqli-brute.py https://example.com/vuln.php?cat= 2 -D target_db -T users --column -C username,password --dump --output-dir ./logs/output.txt
```

## Installation

```bash
git clone https://github.com/yourusername/bsqli-brute.git
cd bsqli-brute
pip install -r requirements.txt
python3 brute.py -h

```

## Disclaimer

This tool is intended for educational purposes and penetration testing in authorized environments only. Misuse of this tool can lead to legal consequences. The authors are not responsible for any damage or unauthorized use.

## License

[MIT](https://github.com/Pintadecal/bsqli-brute/blob/main/LICENSE)

@Pintadecal
