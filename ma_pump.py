#!/usr/bin/env python
# -*- coding: utf-8 -*-


__author__ = 'James Iter'
__date__ = '2018/4/21'
__contact__ = 'james.iter.cn@gmail.com'
__copyright__ = '(c) 2018 by James Iter.'


class MAPump(object):

    def __init__(self, step=None):
        self.step = step
        self.numbers = list()

    def process_data(self, number=None):
        """
        :param number:
        :return:
        """

        assert isinstance(number, (int, float))

        self.numbers.append(number)

        if self.numbers.__len__() < self.step:
            return float(sum(self.numbers)) / self.numbers.__len__()

        else:
            self.numbers = self.numbers[0 - self.step:]
            return float(sum(self.numbers)) / self.numbers.__len__()

