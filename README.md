# ip-enrichment-tool

This IP Enrichment Tool enriches an Excel or CSV file with geolocation and abuse report scores for IP addresses using the AbuseIPDB API. It reads a specified column of IP addresses, queries the AbuseIPDB API for each IP, and adds new columns with the country code and abuse confidence score to the original file.

**Features**

* Supports Excel (.xlsx, .xls) and CSV (.csv) file formats
* Fetches geolocation and abuse report scores for IP addresses from AbuseIPDB
* Adds new columns for CountryCode and AbuseConfidenceScore
* Option to save results to a new file or update the existing file
* Avoids duplicate API requests for the same IP address to save API quota


**Requirements**

* Python 3.x
* Required Python packages:
* pandas
* requests
* openpyxl
* xlrd


**Installation**

```
git clone https://github.com/schafer72/ip-enrichment-tool.git
```


Required Packages:

```
pip install pandas requests openpyxl xlrd
``` 


**Usage**

```
python enrichIPs.py <input_file> <output_file> <ip_column> <api_key> [--update]
```

**Arguments**

* <input_file>: Path to the input Excel or CSV file containing IP addresses.
* <output_file>: Path to the output enriched Excel or CSV file.
* <ip_column>: Name of the column containing IP addresses in the input file.
* <api_key>: Your AbuseIPDB API key.
* --update (optional): If specified, updates the input file instead of saving to a new file.
