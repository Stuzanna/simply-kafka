import requests
import subprocess
import json

def register_schema(schema_registry_url, subject_name, schema_file_path):
    # Read the schema from the file
    with open(schema_file_path, 'r') as schema_file:
        schema_str = schema_file.read()

    # Prepare the curl command
    curl_command = [
        "curl",
        "-X", "POST",
        "-H", "Content-Type: application/vnd.schemaregistry.v1+json",
        "-d", json.dumps({"schema": schema_str}),
        "-w", "%{http_code}",  # Write the HTTP status code to stdout
        "-s",  # Silent mode (don't show progress meter or error messages)
        "-o", "-",  # Write response body to stdout
        f"{schema_registry_url}/subjects/{subject_name}/versions"
    ]
    
    # Execute the curl command
    result = subprocess.run(curl_command, capture_output=True, text=True)

    # Print the response
    http_status_code = result.stdout[-3:].strip()
    response_body = result.stdout[:-3].strip()

    print("HTTP Status Code:", http_status_code)
    print("Response Code:", result.returncode)
    print("Response Body:", response_body)
    print("Response Error:", result.stderr)


def fetch_latest_schema(schema_registry_url: str, subject: str) -> tuple:
    """
    Fetches the latest schema and schema ID for a given subject from the Schema Registry.

    Args:
        schema_registry_url (str): The base URL of the Schema Registry.
        subject (str): The subject for which to fetch the latest schema.

    Returns:
        tuple: A tuple containing:
            - schema_id (int): The ID of the latest schema version.
            - schema_str (str): The latest schema as a string in JSON format.
    
    Raises:
        requests.exceptions.RequestException: If the request to the Schema Registry fails.
        ValueError: If the response from the Schema Registry is invalid or missing the schema ID or schema.

    Example:
        schema_registry_url = "http://localhost:8081"
        subject = "customers-value"
        schema_id, schema_str = fetch_latest_schema(schema_registry_url, subject)
        print(f"Schema ID: {schema_id}")
        print(f"Schema: {schema_str}")
    """

    response = requests.get(f"{schema_registry_url}/subjects/{subject}/versions/latest")
    if response.status_code == 200:
        schema_data = response.json()
        schema_id = schema_data["id"]
        schema_str = schema_data["schema"]

        print(f"Schema ID: {schema_id}")
        print(f"Schema: {schema_str}")
        return schema_id, schema_str

    else:
        raise ValueError(f"Failed to fetch schema: {response.status_code}, {response.text}")
