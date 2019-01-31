from deribit_api import RestClient
#from archon.exchange.deribit.Wrapper import DeribitWrapper
import websocket
import json
import archon.config as config
from datetime import datetime
apikeys = config.parse_toml("apikeys.toml")

k = apikeys["DERIBIT"]["public_key"]
s = apikeys["DERIBIT"]["secret"]
#w = DeribitWrapper(key=k,secret=s)

def main():
    start = datetime.now()
    mtype_count = {}
    client = RestClient(k, s)

    def on_message(ws, message):
        cur = datetime.now()
        since = cur - start
        #print (since)
        m = message
        j = json.loads(m)
        if "notifications" in j.keys():
            n = j["notifications"][0]
            mtype = n["message"]
            r = n["result"]
            instr = (r["instrument"])
            if instr not in mtype_count.keys():
                mtype_count[instr] = 0
            mtype_count[instr] += 1

            print (instr," ",mtype_count[instr]," ",since)
            print (n)

    def on_error(ws, error):
        print(error)

    def on_close(ws):
        print("### closed ###")

    def on_open(ws):
        data = {
            "id": 5533, 
            "action": "/api/v1/private/subscribe",  
            "arguments": {
                #"instrument": ["all"],
                #"instrument": ["BTC-PERPETUAL","BTC-28JUN19-13000-C"],
                "instrument": ["BTC-29MAR19-3000-C"],
                "event": ["order_book"] 
            }
        }
        data['sig'] = client.generate_signature(data['action'], data['arguments'])

        ws.send(json.dumps(data))

    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://www.deribit.com/ws/api/v1/",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()


if __name__ == "__main__":
    main()