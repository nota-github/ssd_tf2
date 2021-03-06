  
'''
A custom Keras layer to perform L2-normalization.
Copyright (C) 2018 Pierluigi Ferrari
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
   http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

import numpy as np
import tensorflow as tf
from tensorflow.keras.layers import InputSpec
from tensorflow.keras.layers import Layer

class L2Normalization(Layer):
    '''
    Performs L2 normalization on the input tensor with a learnable scaling parameter
    as described in the paper "Parsenet: Looking Wider to See Better" (see references)
    and as used in the original SSD model.
    Arguments:
        gamma_init (int): The initial scaling parameter. Defaults to 20 following the
            SSD paper.
    Input shape:
        4D tensor of shape `(batch, channels, height, width)` if `dim_ordering = 'th'`
        or `(batch, height, width, channels)` if `dim_ordering = 'tf'`.
    Returns:
        The scaled tensor. Same shape as the input tensor.
    References:
        http://cs.unc.edu/~wliu/papers/parsenet.pdf
    '''

    def __init__(self, gamma_init=20., **kwargs):
        self.axis = 3
        self.gamma_init = gamma_init
        super(L2Normalization, self).__init__(**kwargs)

    def build(self, input_shape):
        self.input_spec = [InputSpec(shape=input_shape)]
        gamma = self.gamma_init * np.ones((input_shape[self.axis],), dtype='float32')
        self.gamma = tf.Variable(gamma, trainable=True, name='{}_gamma'.format(self.name))
        super(L2Normalization, self).build(input_shape)

    def call(self, x, mask=None):
        output = tf.keras.backend.l2_normalize(x, self.axis)
        return output * self.gamma

    def get_config(self):
        config = {
            'gamma_init': self.gamma_init
        }
        base_config = super(L2Normalization, self).get_config()
        return dict(list(base_config.items()) + list(config.items()))


if __name__ == '__main__':
    layer_l2 = L2Normalization(gamma_init=20., name='conv4_3_norm')
    rand_inp = tf.random.normal([4, 32, 32, 3])
    out = layer_l2(rand_inp)
    print(out)
