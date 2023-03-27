import numpy
import numpy as np
import pickle
from sklearn import linear_model

MODEL = pickle.load(open('sign_compare_model.regr', 'rb'))


def compare_2_vects(vect1: numpy.ndarray, vect2: numpy.ndarray):
    sub = np.absolute(np.subtract(vect1, vect2))
    p = MODEL.predict(sub.reshape(1, -1))
    print(p)
    return p

def compare_with_lst(vect:numpy.ndarray, vects_lst:list[numpy.ndarray]):
    a = sum([compare_2_vects(vect, i) for i in vects_lst])/len(vects_lst)
    print(a)
    return a>40 and a<200
