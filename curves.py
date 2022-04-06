import os
import numpy as np
import pandas as pd
from courbes_cx_cy import INPUT_PATH, OUTPUT_PATH

from preferences import *


class Curves: # drag/lift curves according to time, angle, reynolds

    def __init__ (self, df: pd.DataFrame, reynolds: float, angle: float):
        self.df = df

        self.time = df['Temps']
        self.drag = df['Cx0']
        self.lift = df['Cy0']
        self.reynolds = reynolds
        self.angle = angle

        self.drag_avg = np.average(self.drag)
        self.lift_avg = np.average(self.lift)

        self.repr_short = f'plots-reynolds{int(self.reynolds)}-angle{self.angle}'

    def __repr__ (self):
        return self.repr_short

    def plot (self, **kwargs):
        save = kwargs.get('save', False)
        path = kwargs.get('path', None)
        if save: path = os.path.join(OUTPUT_PATH, self.repr_short)
        if path: save = True
        show = kwargs.get('show', True)

        # plot
        # show

        if save:
            try: os.makedirs(path)
            except: pass
            # TODO: savefig




class Data:

    def __init__ (self):
        self.__curves_list = list()
        self.__curves_dict = dict()  # Curves, ordered by Reynolds number

    def load (self, dirpath=INPUT_FOLDER):
        with os.scandir(dirpath) as files: # add a loop for Reynolds folders

            for file in files:
                name, ext = os.path.splitext(file.name)
                df = pd.read_csv(file.path, sep='\t')

                # Retrieve information
                reynolds = 50000
                angle = float(name.split('_')[-1])

                # Generate Curves object
                curves = Curves(df, reynolds=reynolds, angle=angle)
                
                # Add to self.__curves_list and self.__curves_dict
                self.__curves_list .append(curves)
                if reynolds not in self.__curves_dict.keys: self.__curves_dict[reynolds] = dict()
                self.__curves_dict [reynolds][angle] = curves

    def plot (self):
        for curves in self.__curves_list:
            curves.plot(save=True)  # Individual plot