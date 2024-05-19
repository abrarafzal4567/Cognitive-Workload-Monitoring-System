import configparser
from include import CoapConn

class MainRoboAction:
    # Init function of class
    def __init__(self) -> None:
        self.config = configparser.ConfigParser()
        self.config.read('./settings.ini')
        
    def runCoapConnection(self):
        CoapConnObj = CoapConn.CoapConn(self.config)
        #CoapConnObj.readEEG()
        CoapConnObj.pubsubIt()

if __name__ == '__main__':
    obj = MainRoboAction()
    obj.runCoapConnection()
    