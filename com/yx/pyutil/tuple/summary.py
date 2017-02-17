#!/bin/python
import json
import sys
import time

genre_word = [(genre, word) for genre in brown.categories() for word in brown.words(categories=genre) ]
#先写genre的判断再写依赖于它的word的判断 相当于两次循环