import pandas as pd
import requests
import argparse
import os

# Function to get abuse data for a given IP
def get_abuse_data(ip, api_key):
    url = f'https://api.abuseipdb.com/api/v2/check'
    params = {
        'ipAddress': ip,
        'maxAgeInDays': 90
    }
    headers = {
        'Accept': 'application/json',
        'Key': api_key
    }
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Raise HTTPError for bad responses
        data = response.json().get('data', {})
        return data.get('countryCode', None), data.get('abuseConfidenceScore', None)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for IP {ip}: {e}")
        return None, None

def read_file(file_path):
    file_extension = os.path.splitext(file_path)[1].lower()
    try:
        if file_extension == '.xlsx':
            return pd.read_excel(file_path, engine='openpyxl')
        elif file_extension == '.xls':
            return pd.read_excel(file_path, engine='xlrd')
        elif file_extension == '.csv':
            return pd.read_csv(file_path)
        else:
            print(f"Unsupported file format: {file_extension}")
            return None
    except Exception as e:
        print(f"Error reading the file: {e}")
        return None

def enrich_file(input_file, output_file, ip_column, api_key, update_existing):
    df = read_file(input_file)
    if df is None:
        print("Failed to read the input file.")
        return

    if ip_column not in df.columns:
        print(f"Error: The column {ip_column} does not exist in the input file.")
        return

    # Create new columns for geolocation and abuse score
    if 'CountryCode' not in df.columns:
        df['CountryCode'] = None
    if 'AbuseConfidenceScore' not in df.columns:
        df['AbuseConfidenceScore'] = None

    # Track processed IPs to avoid duplicate API requests
    processed_ips = {}

    # Enrich data
    for index, row in df.iterrows():
        ip = row[ip_column]
        if pd.isna(ip):
            print(f"Warning: Missing IP address at row {index}. Skipping.")
            continue
        if ip in processed_ips:
            country_code, abuse_score = processed_ips[ip]
        else:
            country_code, abuse_score = get_abuse_data(ip, api_key)
            processed_ips[ip] = (country_code, abuse_score)
        
        df.at[index, 'CountryCode'] = country_code
        df.at[index, 'AbuseConfidenceScore'] = abuse_score

    try:
        # Save the enriched file
        if update_existing:
            output_file = input_file

        if output_file.endswith('.xlsx') or output_file.endswith('.xls'):
            df.to_excel(output_file, index=False)
        elif output_file.endswith('.csv'):
            df.to_csv(output_file, index=False)
        else:
            print(f"Unsupported output file format: {os.path.splitext(output_file)[1]}")
            return
    except Exception as e:
        print(f"Error saving the enriched file: {e}")
        return

    print(f"Enriched data has been saved to {output_file}")

def main():
    parser = argparse.ArgumentParser(description="Enrich an Excel or CSV file with IP geolocation and abuse report scores using the AbuseIPDB API.")
    parser.add_argument('input_file', help='Path to the input Excel or CSV file.')
    parser.add_argument('output_file', help='Path to the output enriched Excel or CSV file.')
    parser.add_argument('ip_column', help='Name of the column containing IP addresses.')
    parser.add_argument('api_key', help='Your AbuseIPDB API key.')
    parser.add_argument('--update', action='store_true', help='Update the input file instead of saving to a new file.')

    args = parser.parse_args()

    if not os.path.isfile(args.input_file):
        print(f"Error: The input file {args.input_file} does not exist.")
        return

    enrich_file(args.input_file, args.output_file, args.ip_column, args.api_key, args.update)

if __name__ == "__main__":
    main()
