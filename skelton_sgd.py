#################################
# Your name: Dor Bourshan
#################################


import numpy as np
import numpy.random
from sklearn.datasets import fetch_openml
import sklearn.preprocessing
from numpy import linalg as LA
import matplotlib.pyplot as plt

"""
Please use the provided function signature for the SGD implementation.
Feel free to add functions and other code, and submit this file with the name sgd.py
"""


def helper():
    mnist = fetch_openml('mnist_784', as_frame=False)
    data = mnist['data']
    labels = mnist['target']

    neg, pos = "0", "8"
    train_idx = numpy.random.RandomState(0).permutation(np.where((labels[:60000] == neg) | (labels[:60000] == pos))[0])
    test_idx = numpy.random.RandomState(0).permutation(np.where((labels[60000:] == neg) | (labels[60000:] == pos))[0])

    train_data_unscaled = data[train_idx[:6000], :].astype(float)
    train_labels = (labels[train_idx[:6000]] == pos) * 2 - 1

    validation_data_unscaled = data[train_idx[6000:], :].astype(float)
    validation_labels = (labels[train_idx[6000:]] == pos) * 2 - 1

    test_data_unscaled = data[60000 + test_idx, :].astype(float)
    test_labels = (labels[60000 + test_idx] == pos) * 2 - 1

    # Preprocessing
    train_data = sklearn.preprocessing.scale(train_data_unscaled, axis=0, with_std=False)
    validation_data = sklearn.preprocessing.scale(validation_data_unscaled, axis=0, with_std=False)
    test_data = sklearn.preprocessing.scale(test_data_unscaled, axis=0, with_std=False)
    return train_data, train_labels, validation_data, validation_labels, test_data, test_labels



def SGD_hinge(data:np.ndarray, labels:np.ndarray, C:float, eta_0: float, T: int):
    """
    Implements SGD for hinge loss.
    """
    N = len(data[0]) 
    w_t = np.zeros(N)

    for t in range(1,T+1) :
        eta_t = eta_0 / t
        i = np.random.randint(0, N)
        x_i = data[i]
        y_i = labels[i]
        if np.dot(x_i, w_t) * y_i < 1 : 
            w_t = np.dot(1-eta_t, w_t)   + np.dot((eta_t * C * y_i) , x_i) 
        else : 
            w_t = np.dot(1-eta_t, w_t)
    
    return w_t



def SGD_log(data: np.ndarray, labels:np.ndarray, eta_0: float, T: int):
    """
    Implements SGD for log loss.
    """
    # TODO: Implement me
    pass

#################################



def average_accuracy_plot_eta(number_of_runs: int,  C: float, eta_0_lst: list, T: int, xlim_left, xlim_right) -> float:
    train_data, train_labels, validation_data, validation_labels = helper()[0] , helper()[1] ,helper()[2] ,helper()[3]

    y_axis = [] 

    for eta_0 in eta_0_lst:
        accur = 0 
        for i in range(number_of_runs) :
            w = SGD_hinge(train_data, train_labels, C, eta_0, T)
            accur += accuracy_linear_classifier(w, validation_data, validation_labels)  
        y_axis.append(accur / number_of_runs)

    accu_of_best_eta_0 = 0
    j = -1 
    for i in range(len(y_axis)): 
        if y_axis[i] > accu_of_best_eta_0 :
            accu_of_best_eta_0 = y_axis[i]
            j = i 
    
    print('***********************************************')
    print('The best eta_0 on avarage is: %.6f' % eta_0_lst[j] )
    print('-----------------------------------------------')
    print('The best accuracy on avarage is: %.3f' % accu_of_best_eta_0)
    print('***********************************************')
    
    plt.plot(eta_0_lst, y_axis)   
    plt.xscale('log')
    plt.title("averaging the accuracy on the validation set across 10 runs")
    plt.xlabel("eta_0")
    plt.ylabel("averaging the accuracy on the validation set across 10 runs")
    plt.xlim(xlim_left, xlim_right)
    ticks = [10**i for i in range(-5, 6)]
    labels = ['10^{}'.format(i) for i in range(-5, 6)]
    # plt.xticks(ticks, labels)
    
    plt.legend()
    plt.show()

    return eta_0_lst[j]

def average_accuracy_plot_C(number_of_runs: int,  C_lst: list, eta_0  : float, T: int, xlim_left, xlim_right) -> float:
    train_data, train_labels, validation_data, validation_labels = helper()[0] , helper()[1] ,helper()[2] ,helper()[3]

    y_axis = [] 

    for c in C_lst:
        accur = 0 
        for i in range(number_of_runs) :
            w = SGD_hinge(train_data, train_labels, c, eta_0, T)
            accur += accuracy_linear_classifier(w, validation_data, validation_labels)  
        y_axis.append(accur / number_of_runs)

    accu_of_best_C = 0
    j = -1 
    for i in range(len(y_axis)): 
        if y_axis[i] > accu_of_best_C :
            accu_of_best_C = y_axis[i]
            j = i 
    
    print('***********************************************')
    print('The best C on avarage is: %.6f' % C_lst[j] )
    print('-----------------------------------------------')
    print('The best accuracy on avarage is: %.3f' % accu_of_best_C)
    print('***********************************************')
    
  
    
    plt.plot(C_lst, y_axis)   
    plt.xscale('log')
    plt.title("averaging the accuracy on the validation set across 10 runs")
    plt.xlabel("C")
    plt.ylabel("averaging the accuracy on the validation set across 10 runs")
    ticks = [10**i for i in range(-5, 6)]
    labels = [str(10**(i)) for i in range(-5, 6)]
    plt.xticks(ticks, labels)
    # plt.xlim(xlim_left, xlim_right)
    plt.legend()
    plt.show()
    


def accuracy_linear_classifier(w :np.ndarray , validation_data: np.ndarray, validation_labels:np.ndarray) : 
    linear_classifier = lambda x : np.sign(np.dot(w, x))
    correct_classify = lambda y_hat, y : y_hat == y

    faild_number = 0 
    N = len(validation_data)

    for i in range(N)  :
        if not correct_classify(linear_classifier(validation_data[i]), validation_labels[i]):
            faild_number += 1 

    return 1 - (faild_number / N)

def w_as_picture(best_eta, best_C, T):
    train_data, train_labels, validation_data, validation_labels = helper()[0] , helper()[1] ,helper()[2] ,helper()[3]

    w = SGD_hinge(train_data, train_labels, best_C, best_eta, T)

    plt.imshow(np.reshape(w,(28,28)),interpolation = 'nearest' )
    
    accur = accuracy_linear_classifier(w, validation_data, validation_labels)
    print('***********************************************')
    print('The accuracy of the best classifier: %.6f' % accur )
    print('-----------------------------------------------')
  
    plt.show()





def main() : 
    eta_0_lst = [10**i for i in range(-5,6,1)]
    best_eta = average_accuracy_plot_eta(10, 1, eta_0_lst, 1000,0, 10**5)

    # C_lst = [10**(i) for i in np.arange (-5,6,1)]
    # C_lst = [10**(i) for i in range (-5,6,1)]
    # average_accuracy_plot_C(10, C_lst, 0.97 , 1000, 0, 10**5)

    # best_C = 22.4
    # best_eta = 0.97 

    # w_as_picture(best_eta, best_C, 20000 )





if __name__ == "__main__":
    main()
    