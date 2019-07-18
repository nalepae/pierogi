
import threading as _threading
import asyncio as _asyncio
import websockets as _websockets


class WebSocketServer():
    """
    Web Socket Server

    Best way to use:
    ```
    with WebSocketServer() as web_socket_server:
        web_socket_server.send("message 1")
        # Your stuff here
        web_socket_server.send("message 2")
        # Your stuff here
        web_socket_server.send("message 2")

        # The server will be close (and so data not retrievable any more)
          after the following input
        input("Hit enter to close the websocket server.")
    ```

    If you want to play around in the console or if you don't want to use the
    `with` statement, you can do that:

    ```
    web_socket_server = WebSocketServer()
    web_socket_server.start()

    web_socket_server.send("message 1")
    # Your stuff here
    web_socket_server.send("message 2")
    # Your stuff here
    web_socket_server.send("message 2")

    web_socket_server.stop()
    ```

    WARNING: In this case, don't forget to call the stop method at the end,
             else your program/console will has trouble to close

    To test this web socket server, you can use websocket_client.html in your
    web browser. This webpage has to be loaded AFTER the server is started and
    BEFORE the server is closed. Note that messages sent by the server between
    the server start and this webpage connection WON'T be lost :) !
    """
    __DEFAULT_ADRESS: str = "localhost"
    __DEFAULT_PORT: int = 9559

    def __init__(self, adress: str = __DEFAULT_ADRESS,
                 port: int = __DEFAULT_PORT):
        """Initialization

        Positional arguments:
            adress - The adress
            port   - The port
        """
        self.__adress = adress
        self.__port = port
        self.__clients = set()
        self.__started = False

    async def __handler(self,
                        client: _websockets.protocol.WebSocketCommonProtocol,
                        _) -> None:

        try:
            # TODO: Try to send all in once
            for element in self.__sent:
                await client.send(element)

        except _websockets.ConnectionClosed:
            pass

        self.__clients.add(client)

        has_to_continue = True

        while has_to_continue:
            outgoing = _asyncio.ensure_future(self.__inputs.get())

            dp_ = await _asyncio.wait([outgoing, self.__fut_interrupt],
                                      return_when=_asyncio.FIRST_COMPLETED)

            done, pending = dp_

            if outgoing in pending:
                outgoing.cancel()
                try:
                    await outgoing
                except _asyncio.CancelledError:
                    pass

            if outgoing in done:
                to_send = outgoing.result()
                self.__sent.append(to_send)

                lost_clients = set()
                for client in self.__clients:
                    # TODO: Use a barrier
                    try:
                        await client.send(to_send)

                    except _websockets.ConnectionClosed:
                        lost_clients.add(client)

                if len(lost_clients) != 0:
                    self.__clients -= lost_clients

            if self.__fut_interrupt in done:
                has_to_continue = False

    def start(self) -> None:
        """Start"""
        if self.__started:
            return

        self.__sent = []
        self.__loop: _asyncio.AbstractEventLoop = _asyncio.get_event_loop()
        self.__inputs: _asyncio.Queue = _asyncio.Queue()
        self.__fut_interrupt: _asyncio.Future = self.__loop.create_future()

        self.__serve = _websockets.serve(self.__handler,
                                         self.__adress,
                                         self.__port)

        self.__loop.run_until_complete(self.__serve)

        self.__thread = _threading.Thread(target=self.__loop.run_forever,
                                          name="server")
        self.__thread.start()

        self.__started = True

    def stop(self) -> None:
        """Stop"""
        if not self.__started:
            return

        self.__loop.call_soon_threadsafe(self.__fut_interrupt.set_result, None)
        self.__serve.ws_server.close()
        self.__loop.stop()
        self.__thread.join()

        self.__started = False

    def send(self, message: str) -> None:
        """
        Send a message

        Positional argument:
        message - The message to send
        """
        if not self.__started:
            raise RuntimeError("Server not started. Please call `start`")

        self.__loop.call_soon_threadsafe(self.__inputs.put_nowait, message)

    def __enter__(self):
        self.start()

        return self

    def __exit__(self, *_):
        self.stop()
