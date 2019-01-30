from deribit_api import RestClient
#from archon.exchange.deribit.Wrapper import DeribitWrapper
import websocket
import json
import archon.config as config

apikeys = config.parse_toml("apikeys.toml")

k = apikeys["DERIBIT"]["public_key"]
s = apikeys["DERIBIT"]["secret"]
#w = DeribitWrapper(key=k,secret=s)

def main():
    client = RestClient(k, s)

    def on_message(ws, message):
        m = message
        j = json.loads(m)
        #print (type(j))
        if "notifications" in j.keys():
            n = j["notifications"][0]
            #print (n)
            mtype = n["message"]
            r = n["result"]
            print (mtype)
            print (r["instrument"])
        #n = m["notifications"]
        #print (m) #[0]["message"])
        #print(message)

    def on_error(ws, error):
        print(error)

    def on_close(ws):
        print("### closed ###")

    def on_open(ws):
        data = {
            "id": 5533, 
            "action": "/api/v1/private/subscribe",  
            "arguments": {
                "instrument": ["all"],
                #"instrument": ["BTC-PERPETUAL","BTC-28JUN19-13000-C"],
                #"instrument": ["BTC-28JUN19-13000-C"],
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