# Python program to implement client side of chat room.
import socket
import select
import sys
import pickle
import time
import ast

#dictionary keys
SENDER_ADDRESS_KEY = "SA"
SENDER_ID_KEY = "SID"
MESSAGE_TYPE_KEY = "MT"
MESSAGE_DATA_KEY = "MD"
#player state keys
PLAYER_POSITION_KEY = "PP"
PLAYER_ORIENTATION_KEY = "PO"
PLAYER_COLOR_KEY = "PC"

#message types
SERVER_STATE = 1
GAME_STATE = 10
GAME_EVENT = 11
PLAYER_EVENT = 20
PLAYER_STATE = 21

class FSNMessage:
    def __init__(self, senderID, messageType, extra):
        self.senderAddress = senderAddress
        self.senderID = senderID
        self.messageType = messageType
        self.extra = extra

    def getMessage(message):
        self.senderAddress = message[SENDER_ADDRESS_KEY]
        self.senderID = message[SENDER_ID_KEY]
        self.messageType = message[MESSAGE_TYPE_KEY]
        self.extra = message[MESSAGE_EXTRA_KEY]

    def __str__(self):
        message = {}
        message[SENDER_ADDRESS_KEY] = self.senderAddress
        message[SENDER_ID_KEY] = self.senderID
        message[MESSAGE_TYPE_KEY] = self.messageType
        message[MESSAGE_EXTRA_KEY] = self.extra
        return str(message)


class FSNPlayerState(FSNMessage):
    def __init__(self, senderID, extra, position, orientation, color):
        self.senderAddress = senderAddress
        self.senderID = senderID
        self.messageType = PLAYER_STATE
        self.extra = extra
        self.position = position
        self.orientation = orientation
        self.color = color

    def getMessage(message):
        self.senderAddress = message[SENDER_ADDRESS_KEY]
        self.senderID = message[SENDER_ID_KEY]
        self.messageType = message[MESSAGE_TYPE_KEY]
        self.extra = message[MESSAGE_EXTRA_KEY]
        self.position = message[PLAYER_POSITION_KEY]
        self.orientation = message[PLAYER_ORIENTATION_KEY]
        self.color = message[PLAYER_COLOR_KEY]

    def __str__(self):
        message = {}
        message[SENDER_ADDRESS_KEY] = self.senderAddress
        message[SENDER_ID_KEY] = self.senderID
        message[MESSAGE_TYPE_KEY] = self.messageType
        message[MESSAGE_EXTRA_KEY] = self.extra
        message[PLAYER_POSITION_KEY] = self.position
        message[PLAYER_ORIENTATION_KEY] = self.orientation
        message[PLAYER_COLOR_KEY] = self.color
        return str(message)

        





    
    
