from time import time
import socket


class ClientError(Exception):
    pass


class Client:
    OK_RESPONSE = "ok"
    ERROR_RESPONSE = "error"
    MAX_RESPONSE_SIZE = 1024

    def __init__(self, host, port, timeout=None):
        try:
            self._socket = socket.create_connection((host, port), timeout)
        except socket.error:
            raise ClientError("error while connecting")

    def get(self, query_string):
        metrics = {}
        try:
            self._socket.sendall(f"get {query_string}\n".encode("utf8"))
            res = self._socket.recv(Client.MAX_RESPONSE_SIZE)
            answer = res.decode()
            print(answer)
            if Client.OK_RESPONSE not in answer or Client.ERROR_RESPONSE in answer:
                raise ClientError("server has send response with error")
            
            metrics_list = str(answer).strip("\n").split("\n")
            for metric in metrics_list[1::]:
                raw = metric.split(" ")
                if len(raw) != 3:
                    raise ClientError("invalid data from server")
                else:
                    saved_metrics = metrics.get(raw[0], [])
                    saved_metrics.append((int(raw[2]), float(raw[1])))
                    metrics.update({raw[0]: sorted(saved_metrics)})

            return metrics
        except Exception as ex:
            raise ClientError(ex)
    
    def put(self, key, value, timestamp=None):
        time_to_save = timestamp or int(time())
        
        try:
            self._socket.sendall(f"put {key} {value} {str(time_to_save)}\n".encode("utf8"))
            answer = self._socket.recv(Client.MAX_RESPONSE_SIZE)
            print(answer)
            if Client.OK_RESPONSE not in answer.decode():
                raise ClientError("server has send response with error")
        except Exception as ex:
            raise ClientError(ex)
    
    def __del__(self):
        self._socket.close()

if __name__ == "__main__":
    cl = Client('127.0.0.1', 7777)
    cl.put('test_key', 12.0, 1503319740)
    cl.get('test_key')
