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
    # Configure Pierogi
    pierogi.configure(<nb_epochs>, <nb_batches_per_epoch>)

    # Classic PyTorch training loop
    for epoch in range(1, <nb_epochs> + 1):
        for batch_idx, (data, target) in enumerate(<train_loader>):
            # Put here your classic training step

            # Plot train loss
            pierogi.plot_loss(epoch, batch_idx, <train_loss>, "train")

        # Put here your classic validation loss computation
        pierogi.plot_loss(epoch + 1, 0, <validation_loss>, "validation")

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

# Configure Pierogi
pierogi.configure(<nb_epochs>, <nb_batches_per_epoch>)

# Classic PyTorch training loop
for epoch in range(1, <nb_epochs> + 1):
    for batch_idx, (data, target) in enumerate(<train_loader>):
        # Put here your classic training step

        # Plot train loss
        pierogi.plot_loss(epoch, batch_idx, <train_loss>, "train")

    # Put here your classic validation loss computation
    pierogi.plot_loss(epoch + 1, 0, <validation_loss>, "validation")

pierogi.stop()
```

**WARNING**: In this case, don't forget to call the stop method at the end,
else your program/console will has trouble to close

## Examples

**MNIST** training example is available [here](https://github.com/nalepae/pierogi/blob/master/docs/mnist.py).
This example is directly extracted from official PyTorch example repository, [here](https://github.com/pytorch/examples/blob/master/mnist/main.py).

Modified lines number from the orinal files are: 10, 32, 47, 50, 70, 121 => 123, 126 => 129.
