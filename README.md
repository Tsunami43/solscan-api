```plaintext
░██████╗░█████╗░██╗░░░░░░██████╗░█████╗░░█████╗░███╗░░██╗
██╔════╝██╔══██╗██║░░░░░██╔════╝██╔══██╗██╔══██╗████╗░██║
╚█████╗░██║░░██║██║░░░░░╚█████╗░██║░░╚═╝███████║██╔██╗██║
░╚═══██╗██║░░██║██║░░░░░░╚═══██╗██║░░██╗██╔══██║██║╚████║
██████╔╝╚█████╔╝███████╗██████╔╝╚█████╔╝██║░░██║██║░╚███║
╚═════╝░░╚════╝░╚══════╝╚═════╝░░╚════╝░╚═╝░░╚═╝╚═╝░░╚══╝
```
#

`Solscan API Client` is a Python library for interacting with the Solscan public and pro APIs. This client allows you to access blockchain data and perform various operations via the Solscan platform. The library is designed with an object-oriented approach, making it easy to switch between public and pro API functionalities.

## Installation

To use this library, ensure you have Python version 3.6 or higher installed. You can install using pip:

```bash
pip install git+https://github.com/Tsunami43/solscan-api.git
```

## Usage

### Importing the Library
You can import the Solscan class from the library as follows:
```python
from solscan_api import Solscan
```

### Creating an Instance of Solscan
To create an instance of the Solscan API client, specify the API version ("public" or "pro") and provide a valid API token. Optionally, you can provide a logger instance to capture logs.

```python
# Create a logger (OPTIONAL)
logger = logging.getLogger("SolscanClient")
logging.basicConfig(level=logging.INFO)

# Initialize the Solscan client
solscan_client = Solscan(version="pro", token="your_api_token", logger=logger)
```

### Using the PublicApi Class
You can use the methods from the PublicApi class to access public API data.

Example: Getting Chain Information
```python
chain_info = await solscan_client.chain_info()
print(chain_info)

```
Example: Tool Inspection
```python
inspection_result = await solscan_client.tools_inspect("Some message")
print(inspection_result)
```

### Using the AccountMixin Class
The AccountMixin class adds account-related functionalities to the Solscan client. This includes methods for retrieving account information and exporting transaction data.

Example: Getting Account Information

```python
account_info = await solscan_client.get_account("your_account_public_key")
if account_info:
    print(account_info)
else:
    print("Account not found.")
```
Example: Exporting Transactions
```python
transactions = await solscan_client.export_transactions(
    account="your_account_public_key",
    _type="soltransfer",
    fromTime=1622505600,  # Example start time
)
if transactions:
    print(transactions)
else:
    print("No transactions found or an error occurred.")
```

## Error Handling

The following exceptions may be raised during operations:

* AccountNotFoundData: Raised when the specified account cannot be found.
* ErrorReadResponse: Raised when there is an issue reading the response from the server.
* HTTPRequestError: Raised for general network-related issues during the API request.
* Ensure you have appropriate error handling when using these methods to gracefully manage any issues that arise.
