## Data Streaming the average ETH Gas Estimate using KSQLDB

This repository contains a KSQLDB setup connection that streams the average ETH Gas Estimate using the Ethereum Gas Estimate API as source data.

### Prerequisites

  * [KSQLDB](https://ksqldb.io/quickstart.html) 
  * [Python3](https://www.python.org/downloads/)

### How to send data stream to ksqldb?

1. Make sure you have setup the ksqldb on your system using docker-compose [[Ref.]](https://ksqldb.io/quickstart.html) and the ksqldb instance is up and running.
To verify that, run the command `docker-compose ps`
```c
    Name                 Command            State                     Ports
----------------------------------------------------------------------------------------------
broker          /etc/confluent/docker/run   Up      0.0.0.0:29092->29092/tcp, 9092/tcp
ksqldb-cli      /bin/sh                     Up
ksqldb-server   /usr/bin/docker/run         Up      0.0.0.0:8088->8088/tcp
zookeeper       /etc/confluent/docker/run   Up      0.0.0.0:2181->2181/tcp, 2888/tcp, 3888/tcp
```
2. Make sure all the dependencies are installed by running `pip install -r requirements.txt`

Once the installation is done, run the `main.py` python file.

```python
$ python main.py

2022-08-03 17:51:59,697  Fetching ETH Gas estimate
2022-08-03 17:52:02,364  Received unhandled event <RemoteSettingsChanged changed_settings:{ChangedSetting(setting=SettingCodes.MAX_CONCURRENT_STREAMS, original_value=None, new_value=100), ChangedSetting(setting=SettingCodes._max_header_list_size, original_value=None, new_value=8192)}>
2022-08-03 17:52:02,372  Received unhandled event <SettingsAcknowledged changed_settings:{ChangedSetting(setting=SettingCodes.ENABLE_PUSH, original_value=1, new_value=0)}>
2022-08-03 17:52:02,373  Received unhandled event <SettingsAcknowledged changed_settings:{}>
2022-08-03 17:52:02,489  Received unhandled event <PriorityUpdated stream_id:1, weight:16, depends_on:0, exclusive:False>
2022-08-03 17:52:02,589  [{'seq': 0, 'status': 'ok'}]
```

To verify if the data are sent properly to the stream or not, exec into the ksqldb instance by running.
```bash
docker exec -it ksqldb-cli ksql http://ksqldb-server:8088
```

Inside the container, run the select command to emit the changes in the data stream.

```bash
ksql> select * from eth_gas_stream emit changes;
+------------------+------------------+------------------+------------------+------------------+------------------+
|INSTANT           |FAST              |ECO               |AVG_GAS_ESTIMATE  |BASE_FEE          |PRICE             |
+------------------+------------------+------------------+------------------+------------------+------------------+
|15                |10                |7                 |10                |7                 |1681.08           |
|12                |11                |7                 |10                |8                 |1681.08           |
|15                |10                |7                 |10                |7                 |1681.08           |
|12                |11                |7                 |10                |8                 |1681.08           |
|14                |10                |7                 |10                |7                 |1680.21           |
|15                |10                |7                 |10                |7                 |1681.08           |
|12                |11                |7                 |10                |8                 |1681.08           |
```

### File Structure

- [main.py](./main.py) consists of sections like setting the name of the stream, time interval to fetch the gas rate via the API.

- [utils.py](./app/utils.py) consists of the function to return the gas estimate using the gasprice.io API. It also contains the handler function to handle the Keyboard Interrupt while the main.py program is running.

- [data.py](./app/data.py) consists of the DataStream class that has appropriate methods to set the client URL and perform ksqldb operations.

### Contributions

There are many room for improvements for this repository content, please feel free to contribute.

### References

- [gasprice.io API](https://www.gasprice.io/docs/api)

### Donations

```text
BTC: bc1qvl0hfh474kqskjhg9n2junzlsvdlq7mdu53qdx
ETH: 0x67012D3d4352F57B9C4966b104212d81dc590599
SOL: 693pB8EHihjYteuZZ3wogeQ4fgXdwgPudgmjuubQvidc
```
