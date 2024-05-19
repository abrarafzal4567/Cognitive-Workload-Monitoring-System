import random, time, json
import pandas as pd
import os, csv
import numpy as np

import asyncio
import time
from aiocoap import *

class CoapConn:
    def __init__(self, config) -> None:
        self.GatewayCoap = config["CoapServer"]["GatewayCoap"]
        self.coaphighModeFilePath = config["eeg.device"]["highModeFilePath"]
        self.coapLowModeFilePath = config["eeg.device"]["lowModeFilePath"]
        if os.path.exists("sendingHighFreqEEGGateway.csv"):
            os.remove("sendingHighFreqEEGGateway.csv")
        if os.path.exists("sendingLowFreqEEGGateway.csv"):
            os.remove("sendingLowFreqEEGGateway.csv")
        self.dfh = pd.read_csv(self.coaphighModeFilePath)
        self.dfl = pd.read_csv(self.coapLowModeFilePath)
        self.testsmall = pd.read_csv(self.coaphighModeFilePath)
    
    def pubsubIt(self):
        while True:
            postEEGData = self.readEEG()
            if(postEEGData["dataList"]["dfSeg"] != ""):
                # postEEGData["sendingTimeStamp"] = int( time.time() )
                postEEGData["sendingTimeStamp"] = self.getTimeInMs()
                print("Publishing data to Server :: ", postEEGData)
                asyncio.run(self.coapSend(json.dumps(postEEGData).encode('utf-8')))
                time.sleep(1)

    # Send Data Using COAP Protocol
    async def coapSend(self, postEEGData):
        context = await Context.create_client_context()
        # await asyncio.sleep(10)
        payload = postEEGData
        request = Message(code=PUT, payload=payload, uri=self.GatewayCoap)
        response = await context.request(request).response
        print('Result: %s\n%r'%(response.code, response.payload))

    # Toss Between high and low frequencies
    def coinToss(self):
        returnToss = random.choice(["dfh", "dfl"])
        return returnToss
    
    def getTimeInMs(self):
        from datetime import datetime, timezone, timedelta
        return (datetime.now(timezone.utc) + timedelta(days=3)).timestamp() * 1e3

    def readEEG(self):
        # Testing Section STARTS
        dfSeg = self.dfh.sample()
        dfSeg = dfSeg.values.tolist()[0]
        self.saveSendingHighData(dfSeg)
        payload = {
            "dataList": {
                "dfSeg": dfSeg
            }
        }
        # print("This is the List : ", payload)
        # return payload
        # Testing Section ENDS
        dfSeg = ""
        if(self.coinToss() == "dfh"):
            dfSeg = self.dfh.sample()
            dfSeg = dfSeg.values.tolist()[0]
            self.saveSendingHighData(dfSeg)
        elif(self.coinToss() == "dfl"):
            dfSeg = self.dfl.sample()
            dfSeg = dfSeg.values.tolist()[0]
            self.saveSendingLowData(dfSeg)
        payload = {
            "dataList": {
                "dfSeg": dfSeg
            }
        }
        print("This is the List : ", payload)
        return payload
    
    # Save Sending High Frequency Data into CSV File
    def saveSendingHighData(self, data):
        # print("Saving it into file", data)
        with open('sendingHighFreqEEGGateway.csv', 'a', newline='') as file:
            # Step 4: Using csv.writer to write the list to the CSV file
            writer = csv.writer(file)
            writer.writerow(data) # Use writerow for single list

    # Save Sending Low Frequency Data into CSV File
    def saveSendingLowData(self, data):
        # print("Saving it into file", data)
        with open('sendingLowFreqEEGGateway.csv', 'a', newline='') as file:
            # Step 4: Using csv.writer to write the list to the CSV file
            writer = csv.writer(file)
            writer.writerow(data) # Use writerow for single list

if __name__ == '__main__':
    obj = CoapConn()
    obj.pubsubIt()
