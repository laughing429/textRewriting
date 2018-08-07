"""Module defining encoders."""
from onmt.encoders.encoder import EncoderBase
from onmt.encoders.transformer import TransformerEncoder
from onmt.encoders.rnn_encoder import RNNEncoder
from onmt.encoders.cnn_encoder import CNNEncoder
from onmt.encoders.mean_encoder import MeanEncoder

# from ..encoders.encoder import EncoderBase
# from ..encoders.transformer import TransformerEncoder
# from ..encoders.rnn_encoder import RNNEncoder
# from ..encoders.cnn_encoder import CNNEncoder
# from ..encoders.mean_encoder import MeanEncoder

__all__ = ["EncoderBase", "TransformerEncoder", "RNNEncoder", "CNNEncoder",
           "MeanEncoder"]
