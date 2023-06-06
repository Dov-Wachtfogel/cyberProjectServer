import numpy
import numpy as np
import pickle
from sklearn import linear_model

MODEL = pickle.load(open('sign_compare_model.regr', 'rb'))


def compare_2_vects(vect1: numpy.ndarray, vect2: numpy.ndarray):
    sub = np.absolute(np.subtract(vect1, vect2))
    p = abs(MODEL.predict(sub.reshape(1, -1))-124)
    #print(p)
    return p

def compare_with_lst(vect:numpy.ndarray, vects_lst:list[numpy.ndarray]):
    diff = [compare_2_vects(vect, i) for i in vects_lst]
    a = sum(diff)/len(diff)
    print(a)
    return a<50 , a<75
