import logging
import asyncio
from random import randint
import time, json, csv
import aiocoap.resource as resource
import aiocoap
import configparser
from aiocoap import *
from include import HybridModelCode
from include import sendToThingsboard
# from aiocoap.numbers.contentformat import ContentFormat

class BlockResource(resource.Resource):
    
    def __init__(self):
        super().__init__()
        self.config = configparser.ConfigParser()
        self.config.read('./settings.ini')
        self.tbUri = []
        self.tbUri.append(self.config["TbServer"]["tbUri-001"])
        self.tbUri.append(self.config["TbServer"]["tbUri-002"])
        self.tbUri.append(self.config["TbServer"]["tbUri-003"])
        self.tbUri.append(self.config["TbServer"]["tbUri-004"])
        self.dataArrayLowFreq = []
        self.dataArrayHighFreq = []
        # #############
        # Gateway 2D Array index[0] = Low Freq and index[1] =  
        self.g1 = [[],[]]
        self.g2 = [[],[]]
        self.g3 = [[],[]]
        self.g4 = [[],[]]
        # #############
        self.modelObj = HybridModelCode.HybridModelCode()
        self.obj = sendToThingsboard.sendToThingsboard(self.tbUri)

    async def render_put(self, request):
        msgData = request.payload.decode("utf-8")
        print('PUT payload: %s' % msgData)

        rcDataJson = json.loads(msgData)
        currentTime = self.getTimeInMs()
        # currentTime =  int( time.time())
        sendingTimeStamp = rcDataJson["sendingTimeStamp"]
        latency = currentTime - sendingTimeStamp

        dataList = self.processReceivedData(msgData)
        # print("000000000000000000000000000000000000000000000000000000000 :: ", dataList)
        if(dataList["modRet"] == 0):
            dataList["latency"] = latency
            dataList["gw"] = rcDataJson["GatewayID"]
        # print("FINAL SENDING000000000000000000000000000000000000000000 :: ", dataList)
        await self.obj.main(dataList)
        return aiocoap.Message(code=aiocoap.CHANGED, payload=request.payload)

    def processReceivedData(self, msg):
        # payload = msg.payload.decode()
        payload = msg
        dataList = json.loads(payload)
        if(dataList["GatewayID"] == "gw-001"):
            print("gw-001")
            dataList = dataList["dataList"]["dfSeg"]
            print("Received Data list is :: ", dataList)
            # Sending Latency Time Start
            # ##############################
            dataListLatency = json.loads(payload)
            currentTime = self.getTimeInMs()
            # currentTime = int( time.time())
            sendingTimeStamp = dataListLatency["sendingTimeStamp"]
            latency = currentTime - sendingTimeStamp
            print("Received Time Stamp :: ", sendingTimeStamp, " Current Time Stamp :: ", currentTime, "Latency = ", latency)
            Topic = "main/EEGtoServerLatency"
            dictData = {
                "EEGtoServerLatency": latency
            }
            # self.client.publish(Topic, json.dumps(dictData)) #publish Latency
            # ##############################
            # Sending Latency Time END
            if "_hi" in dataList[0]:
                print("it is High :: ", dataList)
                self.g1[1].append(dataList)
                # self.dataArrayHighFreq.append(dataList)
            elif "_lo" in dataList[0]:
                print("it is low :: ", dataList)
                self.g1[0].append(dataList)
                # self.dataArrayLowFreq.append(dataList)
            # Send to the Model
            # print("Here is the g1 ... ", self.g1)
            try:
                print("Gateway ID is : gw-001", "|| Low Freq Length : ", len(self.g1[0]), "|| High Freq Length : ", len(self.g1[1]))
            except Exception as ex:
                print("Exception is .. ", ex)
            retCalFreq = self.runAImodel("gw-001", self.g1)
            if(retCalFreq != 0):
                print("Calculated Frequency is : ", retCalFreq)
                if(retCalFreq["ind"] == "l"):
                    self.g1[0].clear()
                elif(retCalFreq["ind"] == "h"):
                    self.g1[1].clear()
                retCalFreq["gw"] = "gw-001"
                return retCalFreq
            return {"modRet":0}
        # ############### GW1
        elif(dataList["GatewayID"] == "gw-002"):
            print("gw-002")
            dataList = dataList["dataList"]["dfSeg"]
            print("Received Data list is :: ", dataList)
            # Sending Latency Time Start
            # ##############################
            dataListLatency = json.loads(payload)
            currentTime = self.getTimeInMs()
            # currentTime = int( time.time())
            sendingTimeStamp = dataListLatency["sendingTimeStamp"]
            latency = currentTime - sendingTimeStamp
            print("Received Time Stamp :: ", sendingTimeStamp, " Current Time Stamp :: ", currentTime, "Latency = ", latency)
            Topic = "main/EEGtoServerLatency"
            dictData = {
                "EEGtoServerLatency": latency
            }
            # self.client.publish(Topic, json.dumps(dictData)) #publish Latency
            # ##############################
            # Sending Latency Time END
            if "_hi" in dataList[0]:
                print("it is High :: ", dataList)
                self.g2[1].append(dataList)
                # self.dataArrayHighFreq.append(dataList)
            elif "_lo" in dataList[0]:
                print("it is low :: ", dataList)
                self.g2[0].append(dataList)
                # self.dataArrayLowFreq.append(dataList)
            # Send to the Model
            # print("Here is the g2 ... ", self.g2)
            try:
                print("Gateway ID is : gw-002", "|| Low Freq Length : ", len(self.g2[0]), "|| High Freq Length : ", len(self.g2[1]))
            except Exception as ex:
                print("Exception is .. ", ex)
            retCalFreq = self.runAImodel("gw-002", self.g2)
            if(retCalFreq != 0):
                print("Calculated Frequency is : ", retCalFreq)
                if(retCalFreq["ind"] == "l"):
                    self.g2[0].clear()
                elif(retCalFreq["ind"] == "h"):
                    self.g2[1].clear()
                retCalFreq["gw"] = "gw-002"
                return retCalFreq
            return {"modRet":0}
        # ############# GW3
        elif(dataList["GatewayID"] == "gw-003"):
            print("gw-003")
            dataList = dataList["dataList"]["dfSeg"]
            print("Received Data list is :: ", dataList)
            # Sending Latency Time Start
            # ##############################
            dataListLatency = json.loads(payload)
            currentTime = self.getTimeInMs()
            # currentTime = int( time.time())
            sendingTimeStamp = dataListLatency["sendingTimeStamp"]
            latency = currentTime - sendingTimeStamp
            print("Received Time Stamp :: ", sendingTimeStamp, " Current Time Stamp :: ", currentTime, "Latency = ", latency)
            Topic = "main/EEGtoServerLatency"
            dictData = {
                "EEGtoServerLatency": latency
            }
            # self.client.publish(Topic, json.dumps(dictData)) #publish Latency
            # ##############################
            # Sending Latency Time END
            if "_hi" in dataList[0]:
                print("it is High :: ", dataList)
                self.g3[1].append(dataList)
                # self.dataArrayHighFreq.append(dataList)
            elif "_lo" in dataList[0]:
                print("it is low :: ", dataList)
                self.g3[0].append(dataList)
                # self.dataArrayLowFreq.append(dataList)
            # Send to the Model
            # print("Here is the g3 ... ", self.g3)
            try:
                print("Gateway ID is : gw-003", "|| Low Freq Length : ", len(self.g3[0]), "|| High Freq Length : ", len(self.g3[1]))
            except Exception as ex:
                print("Exception is .. ", ex)
            retCalFreq = self.runAImodel("gw-003", self.g3)
            if(retCalFreq != 0):
                print("Calculated Frequency is : ", retCalFreq)
                if(retCalFreq["ind"] == "l"):
                    self.g3[0].clear()
                elif(retCalFreq["ind"] == "h"):
                    self.g3[1].clear()
                retCalFreq["gw"] = "gw-003"
                return retCalFreq
            return {"modRet":0}
        ###############################################
        # ############# GW4
        elif(dataList["GatewayID"] == "gw-004"):
            print("gw-004")
            dataList = dataList["dataList"]["dfSeg"]
            print("Received Data list is :: ", dataList)
            # Sending Latency Time Start
            # ##############################
            dataListLatency = json.loads(payload)
            currentTime = self.getTimeInMs()
            # currentTime = int( time.time())
            sendingTimeStamp = dataListLatency["sendingTimeStamp"]
            # latency = currentTime - sendingTimeStamp
            latency = currentTime - sendingTimeStamp
            print("Received Time Stamp :: ", sendingTimeStamp, " Current Time Stamp :: ", currentTime, "Latency = ", latency)
            Topic = "main/EEGtoServerLatency"
            dictData = {
                "EEGtoServerLatency": latency
            }
            # self.client.publish(Topic, json.dumps(dictData)) #publish Latency
            # ##############################
            # Sending Latency Time END
            if "_hi" in dataList[0]:
                print("it is High :: ", dataList)
                self.g4[1].append(dataList)
                # self.dataArrayHighFreq.append(dataList)
            elif "_lo" in dataList[0]:
                print("it is low :: ", dataList)
                self.g4[0].append(dataList)
                # self.dataArrayLowFreq.append(dataList)
            # Send to the Model
            # print("Here is the g4 ... ", self.g4)
            try:
                print("Gateway ID is : gw-004", "|| Low Freq Length : ", len(self.g4[0]), "|| High Freq Length : ", len(self.g4[1]))
            except Exception as ex:
                print("Exception is .. ", ex)
            retCalFreq = self.runAImodel("gw-004", self.g4)
            if(retCalFreq != 0):
                print("Calculated Frequency is : ", retCalFreq)
                if(retCalFreq["ind"] == "l"):
                    self.g4[0].clear()
                elif(retCalFreq["ind"] == "h"):
                    self.g4[1].clear()
                retCalFreq["gw"] = "gw-004"
                return retCalFreq
            #################################
            return {"modRet":0}
        
    def runAImodel(self, gw, gwArray):
        # BeforeMRTime = int( time.time())
        BeforeMRTime = self.getTimeInMs()
        if(len(gwArray[0]) > 127):
            print("Low -- gateway is ", gw)
            ###################
           
            ###################
    
            payload = {
                "dataArrayFreq": gwArray[0]
            }
            print("Sending Payload data is :: ", payload)
            CalculatedFreq = self.modelObj.predictFreqValues(payload)

            ###################
            # afterMRTime = int( time.time())
            afterMRTime = self.getTimeInMs()
            calTime = afterMRTime - BeforeMRTime
            
            # TopicCal = "main/ModelCalTime"
            # self.client.publish(TopicCal, json.dumps(dictData)) #publish Model Cal Time
            ###################
            print("Calculate Frequencies", CalculatedFreq)
            print("Publishing data to Server :: ", CalculatedFreq)
            retPayload = {
                "ind": "l",
                "calFreq": CalculatedFreq,
                "ModelCalTime": calTime,
                "modRet":1
            }
            return retPayload
        
        if(len(gwArray[1]) > 127):
            print("High -- gateway is ", gw)
            payload = {
                "dataArrayFreq": gwArray[1]
            }
            print("Sending Payload data is :: ", payload)
            CalculatedFreq = self.modelObj.predictFreqValues(payload)
            afterMRTime = self.getTimeInMs()
            # afterMRTime = int( time.time())
            calTime = afterMRTime - BeforeMRTime
            print("Calculate Frequencies", CalculatedFreq)
            print("Publishing data to Server :: ", CalculatedFreq)
            self.saveSendingResultData(CalculatedFreq)
            # self.dataArrayHighFreq.clear()
            retPayload = {
                "ind": "h",
                "calFreq": CalculatedFreq,
                "ModelCalTime": calTime,
                "modRet":1
            }
            return retPayload
        return 0

    # Save Sending High Frequency Data into CSV File
    def saveSendingResultData(self, data):
        # print("Saving it into file", data)
        with open('CalFreqRobGt.csv', 'a', newline='') as file:
            # Step 4: Using csv.writer to write the list to the CSV file
            writer = csv.writer(file)
            writer.writerow(data) # Use writerow for single list
    
    def getTimeInMs(self):
        from datetime import datetime, timezone, timedelta
        return (datetime.now(timezone.utc) + timedelta(days=3)).timestamp() * 1e3

# logging setup
logging.basicConfig(level=logging.INFO)
# logging.getLogger("coap-server").setLevel(logging.DEBUG)

async def main():
    # Resource tree creation
    root = resource.Site()
    root.add_resource(['other', 'block1'], BlockResource())
    await aiocoap.Context.create_server_context(root)
    # Run forever
    await asyncio.get_running_loop().create_future()

if __name__ == "__main__":
    asyncio.run(main())
