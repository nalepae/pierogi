from .utils.websocket import WebSocketServer as _WebSocketServer
import webbrowser as _webbrowser
import os as _os
import os.path as _path
import json as _json

_LOC = _path.realpath(_path.join(_os.getcwd(), _path.dirname(__file__)))
_WEB_APP_PATH = _os.path.join(_LOC, "webapp", 'pierogi.html')


class Pierogi():

    """
    Plot your training data on your web browser.

    Best way to use:
    ```
    with Pierogi() as pierogi:
        # Your stuff here
        pierogi.append_training_loss(2.1)
        # Your stuff here
        web_socket_server.append_training_loss(1.4)
        # Your stuff here
        web_socket_server.append_training_loss(0.9)

        # Pierogi will be close (and so data not retrievable any more on the
        # web browser) after the following input
        input("Hit enter to stop Pierogi.")
    ```

    If you want to play around in the console or if you don't want to use the
    `with` statement, you can do that:

    ```
    pierogi = Pierogi()
    pierogi.start()

    # Your stuff here
    pierogi.append_training_loss(2.1)
    # Your stuff here
    web_socket_server.append_training_loss(1.4)
    # Your stuff here
    web_socket_server.append_training_loss(0.9)

    pierogi.stop()
    ```

    WARNING: In this case, don't forget to call the stop method at the end,
             else your program/console will has trouble to close

    """

    def __init__(self):
        """Initialization"""
        self.__web_socket_server = _WebSocketServer()

    def start(self):
        """Start and open the web browser"""
        self.__web_socket_server.start()
        _webbrowser.open(_WEB_APP_PATH)

    def stop(self):
        """Stop"""
        self.__web_socket_server.stop()

    def configure(self, nb_epochs=None, nb_batches_per_epoch=None):
        to_send = {}
        if nb_epochs:
            to_send["nb_epochs"] = nb_epochs

        if nb_batches_per_epoch:
            to_send["nb_batches_per_epoch"] = nb_batches_per_epoch

        self.__web_socket_server.send(_json.dumps(to_send))

    def plot_loss(self, epoch, batch, loss, type="train"):
        """Append the train loss

        Positional argument:
        loss - The train loss

        Keyword argument:
        type - Has to be "train" or "validation"
        """
        to_send = {"epoch": epoch, "batch": batch, f"{type}_loss": loss}

        self.__web_socket_server.send(_json.dumps(to_send))

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *_):
        self.stop()
