"""
*  ____           _
* |  _ \ ___   __| |_ __ _   _ _ __ ___
* | |_) / _ \ / _` | '__| | | | '_ ` _ \
* |  __/ (_) | (_| | |  | |_| | | | | | |
* |_|   \___/ \__,_|_|   \__,_|_| |_| |_|
*
* This program is free software: you can redistribute it and/or modify
* it under the terms of the GNU Lesser General Public License as published by
* the Free Software Foundation, either version 3 of the License, or
* (at your option) any later version.
"""
import time
import os
from ..pyraklib.server import PyRakLibServer
from ..pyraklib.server import ServerHandler

from .utils import logger, fs
from .utils.Utils import Utils

from .wizard import wizard

from .lang import base

logo = """
    ____           _                      
   |  _ \ ___   __| |_ __ _   _ _ __ ___  
   | |_) / _ \ / _` | '__| | | | '_ ` _ \ 
   |  __/ (_) | (_| | |  | |_| | | | | | |
   |_|   \___/ \__,_|_|   \__,_|_| |_| |_|
   """


class Server:
    def __init__(self, path, withWizard, isTravisBuild = False):
        super().__init__()
        self.path = path
        self.withWizard = withWizard
        if(withWizard):
            fs.checkAllFiles(path)
        else:
            wizard.skipWizard(path)
        port = 19132
        print(str(logo))
        wizard.isInWizard = False
        logger.log('info',  str(base.get("startingServer")).replace("{ip}", str(Utils.getPrivateIpAddr())).replace("{port}", str(port)))
        logger.log('info', str(base.get("extIpMsg")).replace("{ipPublic}", str(Utils.getPublicIpAddr())))
        logger.log('info', str(base.get("license")))
        server = PyRakLibServer(port=19132)
        handler = ServerHandler(server, None)
        handler.sendOption("name", "MCPE;Podrum powered server;390;1.14.60;0;0;0;PodrumPoweredServer;0")
        if (isTravisBuild):
            print("Build success.")
            os._exit(0)
        else:
            while wizard.isInWizard == False:
                cmd = input('> ')
                command(cmd, True)
                cmd = None
            ticking = True
            while ticking:
                time.sleep(0.002)


def command(string, fromConsole):
    if string.lower() == 'stop':
        logger.log('info', 'Stopping server...')
        Utils.killServer()
    elif string.lower() == '':
        pass
    elif string.lower() == 'help':
        logger.log('info', '/stop: Stops the server')
    else:
        logger.log('error', str(base.get("invalidCommand")))
