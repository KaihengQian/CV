from builtins import range
import numpy as np
from random import shuffle
# from past.builtins import xrange

def softmax_loss_naive(W, X, y, reg):
    """
    Softmax loss function, naive implementation (with loops)

    Inputs have dimension D, there are C classes, and we operate on minibatches
    of N examples.

    Inputs:
    - W: A numpy array of shape (D, C) containing weights.
    - X: A numpy array of shape (N, D) containing a minibatch of data.
    - y: A numpy array of shape (N,) containing training labels; y[i] = c means
      that X[i] has label c, where 0 <= c < C.
    - reg: (float) regularization strength

    Returns a tuple of:
    - loss as single float
    - gradient with respect to weights W; an array of same shape as W
    """
    # Initialize the loss and gradient to zero.
    loss = 0.0
    dW = np.zeros_like(W)

    #############################################################################
    # TODO: 使用显式循环计算softmax损失及其梯度。
    # 将损失和梯度分别保存在loss和dW中。
    # 如果你不小心，很容易遇到数值不稳定的情况。 
    # 不要忘了正则化！                                                           
    #############################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    num_classes = W.shape[1]
    num_train = X.shape[0]
    
    for i in range(num_train):
        scores = X[i].dot(W)
        scores -= np.max(scores)  # 避免遇到数值不稳定的情况
        softmax = np.exp(scores) / np.sum(np.exp(scores))
        loss -= np.log(softmax[y[i]])
        for j in range(num_classes):
            if j == y[i]:
                dW[:,j] += (softmax[j] - 1) * X[i] 
            else: 
                dW[:,j] += softmax[j] * X[i] 
                
    # Right now the loss is a sum over all training examples, but we want it
    # to be an average instead so we divide by num_train.
    loss /= num_train

    # Add regularization to the loss.
    loss += 0.5 * reg * np.sum(W * W)
    
    dW /= num_train
    dW += reg * W

    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    return loss, dW


def softmax_loss_vectorized(W, X, y, reg):
    """
    Softmax loss function, vectorized version.

    Inputs and outputs are the same as softmax_loss_naive.
    """
    # Initialize the loss and gradient to zero.
    loss = 0.0
    dW = np.zeros_like(W)

    #############################################################################
    # TODO: 不使用显式循环计算softmax损失及其梯度。
    # 将损失和梯度分别保存在loss和dW中。
    # 如果你不小心，很容易遇到数值不稳定的情况。 
    # 不要忘了正则化！
    #############################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    num_classes = W.shape[1]
    num_train = X.shape[0]
    scores = X.dot(W)
    scores -= np.max(scores, axis = 1).reshape(-1, 1)  # 避免遇到数值不稳定的情况
    softmax = np.exp(scores) / np.sum(np.exp(scores), axis = 1).reshape(-1,1)
    
    loss -= np.sum(np.log(softmax[range(num_train), y]))
    loss /= num_train
    loss += 0.5 * reg * np.sum(W * W)
    
    softmax[range(num_train), y] -= 1
    dW = X.T.dot(softmax)
    dW /= num_train
    dW += reg * W

    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    return loss, dW
