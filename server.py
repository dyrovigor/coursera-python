import asyncio
from functools import reduce

saved_metrics = {}

SUCCESS_MESSAGE = "ok\n\n"
FAILURE_MESSAGE = "error\nwrong command\n\n"
GET_COMMAND = "get"
PUT_COMMAND = "put"


def get_metrics_handler(metric_key):
    def process_metrics(accumulator, metric):
        metric_timestamp = metric[0]
        metric_value = metric[1]
        return accumulator + f'{metric_key} {metric_value} {metric_timestamp}\n'

    return process_metrics


def process_data(data):
    if not len(data.strip("\n")):
        return FAILURE_MESSAGE
    
    tokens = data.split(" ")
    command = tokens[0]
    
    if command == GET_COMMAND:
        if len(tokens) == 2:
            metric_key = tokens[1].strip()
            
            if metric_key != "*":
                found_metrics = saved_metrics.get(metric_key)
    
                if not found_metrics:
                    return SUCCESS_MESSAGE

                return SUCCESS_MESSAGE[:-1:] + reduce(
                    get_metrics_handler(metric_key),
                    sorted(found_metrics),
                    ""
                ) + "\n"
            else:
                answer = SUCCESS_MESSAGE[:-1:]
                for saved_key, saved_values in saved_metrics.items():
                    answer += reduce(
                        get_metrics_handler(saved_key),
                        sorted(saved_values),
                        ""
                    )
                return answer + "\n"
        else:
            return FAILURE_MESSAGE
    elif command == PUT_COMMAND:
        if len(tokens) == 4:
            try:
                metric_key = tokens[1]
                metric_value = float(tokens[2])
                metric_timestamp = int(tokens[3])
            except ValueError:
                return FAILURE_MESSAGE
            
            saved_values = saved_metrics.get(metric_key, [])
            for i, m in enumerate(saved_values):
                if m[0] == metric_timestamp:
                    saved_values.remove((metric_timestamp, m[1]))
                    saved_values.insert(i, (metric_timestamp, metric_value))
                    return SUCCESS_MESSAGE

            saved_values.append((metric_timestamp, metric_value))
            saved_metrics.update({metric_key: saved_values})
            print(saved_metrics.get(metric_key))
            return SUCCESS_MESSAGE
        else:
            return FAILURE_MESSAGE
    else:
        return FAILURE_MESSAGE


class AsyncServerProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        resp = process_data(data.decode())
        self.transport.write(resp.encode())


def run_server(host, port):
    event_loop = asyncio.get_event_loop()
    server_coroutine = event_loop.create_server(AsyncServerProtocol, host, port)
    server = event_loop.run_until_complete(server_coroutine)

    try:
        event_loop.run_forever()
    except KeyboardInterrupt:
        server.close()
        event_loop.run_until_complete(server.wait_closed())
        event_loop.close()


if __name__ == "__main__":
    run_server('127.0.0.1', 7777)
