import ksql


class DataStream:
    def __init__(self, ksqldb_url):
        self.client = ksql.KSQLAPI(ksqldb_url)

    def create_stream(self, stream_name, topic):
        """This method creates a stream in ksqldb

        Args:
            stream_name (str): Name of the Stream
            topic (str): Name of the Kafka Topic

        Returns:
            response: Response Returned from KSQLDB if any
            excpt: Exception if any
        """
        try:
            response = self.client.ksql(
                f"CREATE STREAM {stream_name} (INSTANT BIGINT, FAST BIGINT, ECO BIGINT, AVG_GAS_ESTIMATE BIGINT, BASE_FEE BIGINT, PRICE DOUBLE) WITH (KAFKA_TOPIC='{topic}', KEY_FORMAT='KAFKA', PARTITIONS=2, VALUE_FORMAT='JSON');")
            return response, None

        except Exception as e:
            return None, e

    def run_ksql_command(self, command):
        """This method runs a ksqldb specific command.

        Args:
            command (str): KSQLDB command to be run

        Returns:
            response: Response Returned from KSQLDB if any
            excpt: Exception if any
        """      
        try:
            response = self.client.ksql(command)
            return response, None

        except Exception as e:
            return None, e

    def run_ksql_query(self, query):
        """This method runs a ksqldb query command.

        Args:
            query (str): KSQLDB query command to be run

        Returns:
            response: Response Returned from KSQLDB if any
            excpt: Exception if any
        """         
        try:
            response = self.client.ksql(query)
            return response, None

        except Exception as e:
            return None, e
