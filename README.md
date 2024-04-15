# SophosAPI-client

This repository contains a Python client for interacting with the Sophos API. It provides functionality to retrieve access tokens, IDs, tenants, and endpoints from the Sophos API.

## Usage

### Clone the repository:

```bash
git clone https://github.com/0xSecureByte/SophosAPI-client.git
```

### Install dependencies:
```bash
pip3 install requests
```

### Update these variables in the `__main__` block with your Sophos API credentials:

- `client_id`
- `client_secret`

### Run the script:
```bash
python3 sophos_api.py
```

**Note:** The responses will be stored in JSON format as follows: `access_token.json`, `whoami.json`, and `endpoints.json`.
