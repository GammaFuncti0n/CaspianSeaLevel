import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

import os
import json
from tqdm import tqdm


class DataVisualizer():
    '''
    Class for visualize data
    '''
    def __init__(self) -> None:
        '''
        Init DataVisualizer
        '''
        pass

    def plot_post_post(self, posts_dir: str, plots_dir: str) -> None:
        '''
        Make set of plots compare post and post
        :params:
            posts_dir: str - directory where contain data from posts
            plots_dir: str - directory where contain plots
        '''
        post_names = os.listdir(posts_dir)
        pass

    def plot_type_1(self) -> None:
        pass