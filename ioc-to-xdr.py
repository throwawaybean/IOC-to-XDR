import csv
from urllib.parse import urlparse

# Function to clean up URL
def clean_url(url):
    parsed_url = urlparse(url)
    if parsed_url.scheme:
        url = parsed_url.netloc
    if parsed_url.path:
        url = parsed_url.netloc + parsed_url.path.split('/')[0]
    return url

# Function to process the CSV file
def process_csv(file_name):
    # Dictionary to hold modified data
    modified_data = {
        "domains": [],
        "IP_ADDRESS/ADRESSE_IP": []
    }

    with open(file_name, newline='') as csvfile:
        reader = csv.reader(csvfile)
        # Skip first three rows
        for _ in range(3):
            next(reader)

        # Process each row
        for row in reader:
            # Skip empty rows
            if not row:
                continue
            
            # Ensure row has at least 2 columns
            if len(row) >= 2:
                data_type = row[0]
                data_value = row[1]

                if data_type == "URL/URL":
                    # Clean URL
                    domain = clean_url(data_value)
                    modified_data["domains"].append(domain)

                elif data_type == "DOMAIN/DOMAINE":
                    # Remove www subdirectory
                    if data_value.startswith("www."):
                        data_value = data_value.replace("www.", "", 1)
                    modified_data["domains"].append(data_value)

                elif data_type == "IP_ADDRESS/ADRESSE_IP":
                    modified_data["IP_ADDRESS/ADRESSE_IP"].append(data_value)

    return modified_data

# Function to generate queries
def generate_queries(data):
    ips_query = '''
config case_sensitive = false  
| dataset = xdr_data  
| filter event_type = ENUM.STORY  
| filter action_remote_ip in ({})
| fields _time, agent_hostname, actor_process_image_name, action_local_ip, action_remote_ip, action_remote_port, dns_query_name, action_external_hostname
'''.format(', '.join(['"{}"'.format(ip) for ip in data["IP_ADDRESS/ADRESSE_IP"]]))

    domains_query = '''
config case_sensitive = false  
| dataset = xdr_data  
| filter event_type = ENUM.STORY  
| filter {}
| fields _time, agent_hostname, actor_process_image_name, action_local_ip, action_remote_ip, action_remote_port, dns_query_name, action_external_hostname
'''.format(' OR '.join(['dns_query_name ~= "{}"'.format(domain) for domain in data["domains"]]))

    urls_query = '''
config case_sensitive = false  
| dataset = xdr_data  
| filter event_type = ENUM.STORY  
| filter {}
| fields _time, agent_hostname, actor_process_image_name, action_local_ip, action_remote_ip, action_remote_port, dns_query_name, action_external_hostname
'''.format(' OR '.join(['action_external_hostname ~= "{}"'.format(url) for url in data["domains"]]))

    return ips_query, domains_query, urls_query

# Main function
def main():
    file_name = input("Enter the CSV file name: ")
    data = process_csv(file_name)
    ips_query, domains_query, urls_query = generate_queries(data)
    print("ips_query:\n", ips_query)
    print("\ndomains_query:\n", domains_query)
    print("\nurls_query:\n", urls_query)

if __name__ == "__main__":
    main()
