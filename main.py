from app.data import DataStream
from app.utils import *
from time import sleep


################################################################
#                       VARIABLES                              #
################################################################

STREAM_NAME = "eth_gas_stream"
TOPIC_NAME = "eth_gas_estimate"
KSQL_DB_URL = "http://localhost:8088"
GAS_ESTIMATE_API_URL = "https://api.gasprice.io/v1/estimates"
FETCH_DATA_INTERVAL = 30  # in seconds

if __name__ == '__main__':
    stream_data_list = []
    # Initiliaze the ksqldb client
    ds = DataStream(KSQL_DB_URL)
    # Store the value of Describe Command.
    describe_stream_cmd = f"DESCRIBE {STREAM_NAME}"
    # Store the value of Run KSQLDB Command.
    desc_output, excpt = ds.run_ksql_command(describe_stream_cmd)

    if desc_output is None:
        create_stream_result, excpt = ds.create_stream(
            STREAM_NAME, TOPIC_NAME)

    try:
        while True:
            data, excpt = get_gas_estimate(GAS_ESTIMATE_API_URL)
            average_gas_estimate = (int(
                data["instant"]["feeCap"])+int(data["fast"]["feeCap"])+int(data["eco"]["feeCap"]))//3
            if excpt is None:
                # Create the Stream Data Row Value
                stream_data_row_val = {"INSTANT": int(data["instant"]["feeCap"]), "FAST": int(data["fast"]["feeCap"]), "ECO": int(
                    data["eco"]["feeCap"]), "AVG_GAS_ESTIMATE": average_gas_estimate, "BASE_FEE": int(data["baseFee"]), "PRICE": data["ethPrice"]}
                # Append it to the Stream Data List
                stream_data_list.append(stream_data_row_val)
                # Insert the row to the specific stream
                insert_status = ds.client.inserts_stream(
                    STREAM_NAME, stream_data_list)
                logging.info(insert_status)
                sleep(FETCH_DATA_INTERVAL)

    except Exception as e:
        logging.warning(e)
