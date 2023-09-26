

import abc
from typing import Callable,Any,Tuple,Iterable

class TableABC:
    @abc.abstractmethod
    def count(self):
        pass

    @abc.abstractmethod
    def map(self,func: Callable[[Any,Any], Tuple[Any,Any]]):
        '''
        :param func: (k,v) -> (new_k, new_v)
        :return:
        '''
        pass

    @abc.abstractmethod
    def mapvalues(self,func: Callable[[Any], Any]):
        '''
        :param func: v -> new_v
        :return:
        '''
        pass

    @abc.abstractmethod
    def reduce(self, func: Callable[[Any,Any],Any]):
        '''

        :param func:  a binary fuction which reduce two value into one
        :return: any
        '''
        pass

    @abc.abstractmethod
    def join(self,other: 'TableABC', func: Callable[[Any,Any],Any] = lambda v1,v2:v1):
        '''

        :param other:
        :param func:
        :return: TableABC
        '''
        pass

    @abc.abstractmethod
    def subtractByKey(self,other:'TableABC'):
        '''

        :param other:
        :return: TableABC
        '''
        pass

    @abc.abstractmethod
    def filter(self, func: Callable[[Any,Any],bool]):
        '''

        :param func:
        :return: TableABC
        '''
        pass

    @abc.abstractmethod
    def union(self,other: 'TableABC', func: Callable[[Any,Any],Any] = lambda v1,v2:v1):
        '''
        :param other:
        :param func:
        :return:  TableABC
        '''
        pass

    @abc.abstractmethod
    def mapRedecuePartitions(self,mapper:Callable[[iter],list],
                             reducer: Callable[[object,object],object]):
        '''

        :param mapper:
        :param reducer:
        :return: TableABC
        '''
        pass


    @abc.abstractmethod
    def applyPartitions(self,func:Callable[[iter],object]):
        '''
        :param func:
        :return: TableABC
        '''
        pass

    @abc.abstractmethod
    def flatMap(self,func: Callable[[object,object],object]):
        '''

        :param func:
        :return: TableABC
        '''
        pass

    @abc.abstractmethod
    def take(self,n=1):
        '''

        :param n: number of data to take
        :return: list
        '''
        pass

    @staticmethod
    @abc.abstractmethod
    def paralleize(data:Iterable, include_key: bool, partition: int = None):
        '''

        :param data:
        :param include_key:
        :param partition:
        :return: TableABC
        '''
        pass

    @abc.abstractmethod
    def first(self):
        '''

        :return: (k,v) tuple
        '''
        pass

    @abc.abstractmethod
    def collect(self):
        '''

        :return: list
        '''
        pass

    @abc.abstractmethod
    def persist(self):
        '''

        :return: TableABC
        '''
        pass


class Instance:
    def __init__(self, weight: float = None, features=None, label:int = None):
        '''

        :param weight:
        :param features:
        :param label:
        '''
        self.weight = weight
        self.features = features
        self.label = label


    def set_weight(self,weight=1.0):
        self.weight = weight

    def set_label(self,label=1):
        self.label = label

    def set_featurs(self, features):
        self.features = features

    def __repr__(self):
        return str({
            "weight": self.weight,
            "features": self.features,
            "label": self.label
        })