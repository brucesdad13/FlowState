# Python program to implement client side of chat room.
import socket
import select
import sys
import pickle
import time
import ast

#dictionary keys
SENDER_ID_KEY = "SID"
MESSAGE_TYPE_KEY = "MT"
MESSAGE_DATA_KEY = "MD"
MESSAGE_EXTRA_KEY = "MX"

#server event keys
SERVER_EVENT_TYPE_KEY = "SET"
PLAYER_EVENT_TYPE_KEY = "PET"

#message types
SERVER_STATE = 1
SERVER_EVENT = 2
GAME_STATE = 10
GAME_EVENT = 11
PLAYER_STATE = 20
PLAYER_EVENT = 21


class Message:
    def __init__(self, senderID, messageType, extra=None):
        self.senderID = senderID
        self.messageType = messageType
        self.extra = extra

    def getMessage(message):
        Message.senderID = message[SENDER_ID_KEY]
        Message.messageType = message[MESSAGE_TYPE_KEY]
        Message.extra = message[MESSAGE_EXTRA_KEY]

    def __str__(self):
        message = {}
        message[SENDER_ID_KEY] = self.senderID
        message[MESSAGE_TYPE_KEY] = self.messageType
        message[MESSAGE_EXTRA_KEY] = self.extra
        return str(message)
    
class ServerEvent:
    #server event types
    PLAYER_JOINED = 0
    PLAYER_LEFT = 1
    SERVER_QUIT = 2
    
    def __init__(self, eventType, extra=None):
        self.messageType = SERVER_EVENT_TYPE_KEY
        self.eventType = eventType
        self.extra = extra

    def getMessage(message):
        obj = ServerEvent(message[SERVER_EVENT_TYPE_KEY], message[MESSAGE_EXTRA_KEY])
        return obj

    def __str__(self):
        message = {}
        message[MESSAGE_TYPE_KEY] = self.messageType
        message[SERVER_EVENT_TYPE_KEY] = self.eventType
        message[MESSAGE_EXTRA_KEY] = self.extra
        return str(message)

class ServerState(Message):
    #player state keys
    PLAYER_STATES_KEY = "PS"
    def __init__(self, playerStates, extra=None):
        self.messageType = SERVER_STATE
        self.playerStates = playerStates
        self.extra = extra

    def getMessage(message):
        obj = ServerState(message[ServerState.PLAYER_STATES_KEY],message[MESSAGE_EXTRA_KEY])
        return obj

    def __str__(self):
        message = {}
        message[MESSAGE_TYPE_KEY] = self.messageType
        message[ServerState.PLAYER_STATES_KEY] = self.playerStates
        message[MESSAGE_EXTRA_KEY] = self.extra
        return str(message)

class PlayerState(Message):
    #player state keys
    PLAYER_POSITION_KEY = "PP"
    PLAYER_ORIENTATION_KEY = "PO"
    PLAYER_COLOR_KEY = "PC"
    def __init__(self, senderID, extra, position, orientation, color):
        self.senderID = senderID
        self.messageType = PLAYER_STATE
        self.extra = extra
        self.position = position
        self.orientation = orientation
        self.color = color

    def getMessage(message):
        obj = PlayerState(message[SENDER_ID_KEY],message[MESSAGE_EXTRA_KEY],message[PlayerState.PLAYER_POSITION_KEY],message[PlayerState.PLAYER_ORIENTATION_KEY],message[PlayerState.PLAYER_COLOR_KEY])
        return obj

    def __str__(self):
        message = {}
        message[SENDER_ID_KEY] = self.senderID
        message[MESSAGE_TYPE_KEY] = self.messageType
        message[MESSAGE_EXTRA_KEY] = self.extra
        message[self.PLAYER_POSITION_KEY] = self.position
        message[self.PLAYER_ORIENTATION_KEY] = self.orientation
        message[self.PLAYER_COLOR_KEY] = self.color
        return str(message)
    
class PlayerEvent:
    #player event types
    PLAYER_JOINED = 0
    PLAYER_QUIT = 1
    
    def __init__(self, eventType, senderID, extra=None):
        self.messageType = PLAYER_EVENT
        self.eventType = eventType
        self.senderID = senderID
        self.extra = extra

    def getMessage(message):
        obj = PlayerEvent(message[PLAYER_EVENT_TYPE_KEY], message[SENDER_ID_KEY], message[MESSAGE_EXTRA_KEY])
        return obj

    def __str__(self):
        message = {}
        message[MESSAGE_TYPE_KEY] = self.messageType
        message[SENDER_ID_KEY] = self.senderID
        message[PLAYER_EVENT_TYPE_KEY] = self.eventType
        message[MESSAGE_EXTRA_KEY] = self.extra
        return str(message)    

        





    
    
