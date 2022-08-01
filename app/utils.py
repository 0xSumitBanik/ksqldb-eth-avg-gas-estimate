import requests
import logging
import signal

FORMAT = '%(asctime)-15s  %(message)s'
logging.basicConfig(level=logging.INFO,format=FORMAT)

def get_gas_estimate(URL):
    """ This functions returns the estimated gas fee as returned by the API URL.

    Args:
        URL (str): URL of the API to be called

    Returns:
        result: Result of the API call
    """
    try:
        logging.info("Fetching ETH Gas estimate")
        response = requests.get(URL)
        result = response.json()["result"]
        return result, None

    except Exception as e:
        logging.info(e)
        return None, e

 
def handler(signum, frame):
    response = input("Do you really want to exit? (y/n) ")
    if response.lower() == 'y':
        exit(1)
 
signal.signal(signal.SIGINT, handler)       