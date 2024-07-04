from quixstreams import Application
import json
import time

# Consumer based off the Quix model, use of streaming data frame (SDF)
# Application top level object

app = Application (
    broker_address = "localhost:19092",
    loglevel = "DEBUG",
    consumer_group = "stu_consumer_group",
    auto_offset_reset = "earliest"
)


max_records = 1000  # Maximum number of records to process
start_time = time.time()  # Start time for elapsed time measurement
max_duration = 100 # max running time

records_processed = 0

with app.get_consumer() as consumer:
    consumer.subscribe(["customers"]) # subscribing to a topic

    while True:
        msg = consumer.poll(1)
        # breakpoint() # add for debugging
        if msg is None:
            print("Waiting for message...")
        elif msg.error() is not None:
            raise Exception(msg.error())
        # else:
        #     breakpoint() # add for debugging
        else:
            key = msg.key().decode('utf8')
            value = json.loads(msg.value())
            offset = msg.offset()

            print(f"{offset} {'|'} {key} {'|'} {value} {'|'}")
            records_processed += 1

        if records_processed >= max_records or time.time() - start_time >= max_duration:
                print("Maximum records or time limit reached. Exiting...")
                break
