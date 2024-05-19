import asyncio
import json
from aiocoap import *
import random

class sendToThingsboard:
    def __init__(self, TbUri) -> None:
        self.TbUri = TbUri
        pass

    async def main(self, dataRec):
        context = await Context.create_client_context()
        # await asyncio.sleep(2)
        xVal = random.randint(0,9)
        print("Sending data is ------------------------- ", dataRec)
        if(dataRec["modRet"] != 0):
            if(dataRec["gw"] == "gw-001"):
                TbGwUri = self.TbUri[0]
            elif(dataRec["gw"] == "gw-002"):
                TbGwUri = self.TbUri[1]
            elif(dataRec["gw"] == "gw-003"):
                TbGwUri = self.TbUri[2]
            elif(dataRec["gw"] == "gw-004"):
                TbGwUri = self.TbUri[3]
            payload = {
                "key": dataRec
            }
            payload = json.dumps(payload).encode("utf-8")
            request = Message(code=POST, payload=payload, uri=TbGwUri)
            response = await context.request(request).response
            print("Result: %s\n%r"%(response.code, response.payload))
        else:
            if(dataRec["gw"] == "gw-001"):
                TbGwUri = self.TbUri[0]
            elif(dataRec["gw"] == "gw-002"):
                TbGwUri = self.TbUri[1]
            elif(dataRec["gw"] == "gw-003"):
                TbGwUri = self.TbUri[2]
            elif(dataRec["gw"] == "gw-004"):
                TbGwUri = self.TbUri[3]
            payload = {
                "NetParams": dataRec
            }
            payload = json.dumps(payload).encode("utf-8")
            request = Message(code=POST, payload=payload, uri=TbGwUri)
            response = await context.request(request).response
            print("Result: %s\n%r"%(response.code, response.payload))



if __name__ == '__main__':
    obj = sendToThingsboard()
    asyncio.run(obj.main())