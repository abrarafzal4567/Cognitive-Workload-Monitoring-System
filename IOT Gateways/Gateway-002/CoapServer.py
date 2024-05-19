import datetime, json
import logging
import asyncio
import aiocoap.resource as resource
# from aiocoap.numbers.contentformat import ContentFormat
import aiocoap
import configparser
from aiocoap import *

from random import randrange

class BlockResource(resource.Resource):
    
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('./settings.ini')
        self.GatewayID = self.config["GatewaySettings"]["GatewayID"]
        self.AIServerURI = self.config["GatewaySettings"]["AIServerURI"]
        super().__init__()

    async def render_put(self, request):
        print("Received PUT payload is : ", request.payload.decode("utf-8"))
        payload = json.loads(request.payload.decode("utf-8"))
        payload.update( {"GatewayID" : self.GatewayID} )
        print("Ready to send to AI-Server :: ", payload)
        await self.main123(json.dumps(payload).encode("utf-8"))
        return aiocoap.Message(code=aiocoap.CHANGED, payload=request.payload)
    
    async def main123(self, payload):
        context = await Context.create_client_context()
        # await asyncio.sleep(2)
        request = Message(code=PUT, payload=payload, uri=self.AIServerURI)
        response = await context.request(request).response
        print('Result: %s\n%r'%(response.code, response.payload))

# logging setup
logging.basicConfig(level=logging.INFO)
# logging.getLogger("coap-server").setLevel(logging.DEBUG)

async def main():
    # Resource tree creation
    root = resource.Site()
    root.add_resource(['other', 'block'], BlockResource())
    await aiocoap.Context.create_server_context(root)
    await asyncio.get_running_loop().create_future()

if __name__ == "__main__":
    asyncio.run(main())
