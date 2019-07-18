# Pierogi

**Pierogi** is a tool to plot your model training loss curve, in real time, directly in your web browser.

<table>
<tr>
  <td>Latest Release</td>
  <td>
    <a href="https://pypi.org/project/pierogi/">
    <img src="https://img.shields.io/pypi/v/pierogi.svg" alt="latest release" />
    </a>
  </td>
</tr>
<tr>
  <td>License</td>
  <td>
    <a href="https://github.com/nalepae/pierogi/blob/master/LICENSE">
    <img src="https://img.shields.io/pypi/l/pierogi.svg" alt="license" />
    </a>
  </td>
</tr>
</table>

![Training MNIST](https://github.com/nalepae/pierogi/blob/master/docs/mnist_train.gif)

## Installation

`$ pip install pierogi [--user]`

## How to use it
### 1. Recommanded way

```python
from pierogi.pierogi import Pierogi

with Pierogi() as pierogi:
    # Your stuff here
    pierogi.append_training_loss(2.1)
    # Your stuff here
    web_socket_server.append_training_loss(1.4)
    # Your stuff here
    web_socket_server.append_training_loss(0.9)

    # Pierogi will be closed (and so data not retrievable any more on the
    # web browser) after the following input
    input("Hit enter to stop Pierogi.")
```

As soon as you enter in the `with` section, your web browser will open.

### 2. Less recommanded way, but could be useful if you want to play with **Pierogi** directly in the console
```python
from pierogi.pierogi import Pierogi

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

**WARNING**: In this case, don't forget to call the stop method at the end, 
else your program/console will has trouble to close

