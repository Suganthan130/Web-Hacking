import requests
import argparse

# Define your XSS test payload
xss_payload = '"><h>sn130hk</h>'

# ANSI color codes
RED = '\033[91m'
GREEN = '\033[92m'
RESET = '\033[0m'

# Function to check if the payload is reflected in the URL response
def check_reflected_xss(url, output_file):
    if "fuzz" in url:  # Ensure the placeholder 'fuzz' exists
        print(f"Checking URL: {url}")
        # Replace the 'fuzz' placeholder with the XSS payload
        test_url = url.replace("fuzz", xss_payload)
        try:
            response = requests.get(test_url)
            # Check if the payload appears in the response (indicating reflected XSS)
            if xss_payload in response.text:
                result = f"Possible reflected XSS vulnerability detected in: {test_url}\n"
                print(f"{RED}{result.strip()}{RESET}")
                output_file.write(result)
            else:
                result = f"No reflected XSS detected in: {test_url}\n"
                print(f"{GREEN}{result.strip()}{RESET}")
                output_file.write(result)
        except requests.exceptions.RequestException as e:
            result = f"Error testing URL {test_url}: {e}\n"
            print(result.strip())
            output_file.write(result)

# Function to handle the file reading and writing
def check_urls_from_file(input_file, output_file):
    with open(input_file, 'r') as file:
        urls = file.readlines()
        for url in urls:
            url = url.strip()  # Remove any extra spaces or newlines
            check_reflected_xss(url, output_file)

# Main function to parse command-line arguments and call the checking function
def main():
    parser = argparse.ArgumentParser(description="Check URLs for reflected XSS vulnerability.")
    parser.add_argument('-i', '--input', required=True, help="Input file containing URLs to check.")
    parser.add_argument('-o', '--output', required=True, help="Output file to write the results.")

    args = parser.parse_args()

    # Open the output file for writing results
    with open(args.output, 'w') as output_file:
        check_urls_from_file(args.input, output_file)

if __name__ == "__main__":
    main()
