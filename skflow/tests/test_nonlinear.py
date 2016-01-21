#  Copyright 2015-present Scikit Flow Authors. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import random

from sklearn import datasets
from sklearn.metrics import accuracy_score, mean_squared_error

import tensorflow as tf

import skflow

class NonLinearTest(tf.test.TestCase):

    def testIris(self):
        random.seed(42)
        iris = datasets.load_iris()
        classifier = skflow.TensorFlowDNNClassifier(
            hidden_units=[10, 20, 10], n_classes=3)
        classifier.fit(iris.data, iris.target)
        score = accuracy_score(iris.target, classifier.predict(iris.data))
        self.assertGreater(score, 0.5, "Failed with score = {0}".format(score))
        weights = classifier.weights_
        self.assertEqual(weights[0].shape, (4, 10))
        self.assertEqual(weights[1].shape, (10, 20))
        self.assertEqual(weights[2].shape, (20, 10))
        self.assertEqual(weights[3].shape, (10, 3))
        biases = classifier.bias_
        self.assertEqual(len(biases), 4)

    def testBoston(self):
        random.seed(42)
        boston = datasets.load_boston()
        regressor = skflow.TensorFlowDNNRegressor(
            hidden_units=[10, 20, 10], n_classes=0,
            batch_size=boston.data.shape[0],
            steps=200, learning_rate=0.001)
        regressor.fit(boston.data, boston.target)
        score = mean_squared_error(
            boston.target, regressor.predict(boston.data))
        self.assertLess(score, 100, "Failed with score = {0}".format(score))
        weights = regressor.weights_
        self.assertEqual(weights[0].shape, (13, 10))
        self.assertEqual(weights[1].shape, (10, 20))
        self.assertEqual(weights[2].shape, (20, 10))
        self.assertEqual(weights[3].shape, (10, 1))
        biases = regressor.bias_
        self.assertEqual(len(biases), 4)


if __name__ == "__main__":
    tf.test.main()
