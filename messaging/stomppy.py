"""
This class add support for Message module in stomppy default listener.
It can be passed directly to :py:func:`Connection.set_listener`.

Copyright (C) CERN 2013-2021
"""

from messaging.message import Message


class MessageListener(object):
    """
    This class add support for Message module in stomppy default listener.
    It can be passed directly to Connection.set_listener().
    """
    def on_connecting(self, host_and_port):
        """
        Called by the STOMP connection once a TCP/IP connection to the
        STOMP server has been established or re-established. Note that
        at this point, no connection has been established on the STOMP
        protocol level. For this, you need to invoke the "connect"
        method on the connection.

        :param host_and_port: a tuple containing the host name and port
        number to which the connection has been established
        """
        pass

    def on_connected(self, headers, body):
        """ Translate standard call to custom one. """
        self.connected(Message(header=headers, body=body.decode()))

    def connected(self, message):
        """
        Called by the STOMP connection when a CONNECTED frame is
        received, that is after a connection has been established or
        re-established.

        :param message: the message received from server
        """
        pass

    def on_disconnected(self):
        """
        Called by the STOMP connection when a TCP/IP connection to the
        STOMP server has been lost.  No messages should be sent via
        the connection until it has been reestablished.
        """
        pass

    def on_heartbeat_timeout(self):
        """
        Called by the STOMP connection when a heartbeat message has not been
        received beyond the specified period.
        """
        pass

    def on_message(self, headers, body):
        """ Translate standard call to custom one. """
        self.message(Message(header=headers, body=body.decode()))

    def message(self, message):
        """
        Called by the STOMP connection when a MESSAGE frame is
        received.

        :param message: the message received from server
        """
        pass

    def on_receipt(self, headers, body):
        """ Translate standard call to custom one. """
        self.receipt(Message(header=headers, body=body.decode()))

    def receipt(self, message):
        """
        Called by the STOMP connection when a RECEIPT frame is
        received, sent by the server if requested by the client using
        the 'receipt' header.

        :param message: the message received from server
        """
        pass

    def on_error(self, headers, body):
        """ Translate standard call to custom one. """
        self.error(Message(header=headers, body=body.decode()))

    def error(self, message):
        """
        Called by the STOMP connection when an ERROR frame is
        received.

        :param message: the message received from server
        """
        pass

    def on_send(self, headers, body):
        """ Translate standard call to custom one. """
        self.send(Message(header=headers, body=body.decode()))

    def send(self, message):
        """
        Called by the STOMP connection when it is in the process
        of sending a message.

        :param message: the message being sent to server
        """
        pass
