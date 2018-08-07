""" Main entry point of the ONMT library """
from __future__ import division, print_function

import onmt.inputters
import onmt.encoders
import onmt.decoders
import onmt.models
import onmt.utils
import onmt.modules
from onmt.trainer import Trainer
import sys
import onmt.utils.optimizers
utils.optimizers.Optim = utils.optimizers.Optimizer
sys.modules["Optim"] = utils.optimizers

# For Flake
__all__ = [inputters, encoders, decoders, models,
           utils, modules, "Trainer"]

__version__ = "0.2.0"
