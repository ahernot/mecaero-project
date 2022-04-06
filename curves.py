import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# from courbes_cx_cy import INPUT_PATH, OUTPUT_PATH

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

    def plot_individual (self, **kwargs):
        figsize = kwargs.get('figsize', (20, 10))
        save = kwargs.get('save', False)
        path = kwargs.get('path', None)
        if path: save = True
        show = kwargs.get('show', True)

        # Lift plot
        plt.figure(figsize=figsize)
        plt.plot(self.time, self.lift, label=self.repr_short)
        plt.xlabel('Time [s]')
        plt.ylabel('Lift [N]')
        if show: plt.show()
        if save:
            if not path: path = os.path.join(OUTPUT_PATH, f'{self.repr_short}/lift.jpg')
            try: os.makedirs(path)
            except: pass
            plt.savefig(path, bbox_inches='tight')

        # Drag plot
        plt.figure(figsize=figsize)
        plt.plot(self.time, self.drag, label=self.repr_short)
        plt.xlabel('Time [s]')
        plt.ylabel('Drag [N]')
        if show: plt.show()
        if save:
            if not path: path = os.path.join(OUTPUT_PATH, f'{self.repr_short}/drag.jpg')
            try: os.makedirs(path)
            except: pass
            plt.savefig(path, bbox_inches='tight')    




class Data:

    def __init__ (self):
        self.__curves_list = list()
        self.__curves_dict = dict()  # Curves, ordered by Reynolds number

    def load (self, dirpath=INPUT_PATH):
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
                if reynolds not in self.__curves_dict.keys(): self.__curves_dict[reynolds] = dict()
                self.__curves_dict [reynolds][angle] = curves

    def plot_all (self, **kwargs):
        for curves in self.__curves_list:
            curves.plot_individual(**kwargs)  # Individual plot

    def plot_drags (self, **kwargs):

        # Unpack kwargs
        figsize = kwargs.get('figsize', (20, 10))
        save = kwargs.get('save', False)
        path = kwargs.get('path', None)
        if path: save = True
        show = kwargs.get('show', True)

        plt.figure(figsize=figsize)
        for curves in self.__curves_list:
        

    def plot_avgs_angle (self, **kwargs):

        # Unpack kwargs
        figsize = kwargs.get('figsize', (20, 10))
        save = kwargs.get('save', False)
        path = kwargs.get('path', None)
        if path: save = True
        show = kwargs.get('show', True)

        # Unpack angles, lifts, drags
        angles, lifts, drags = list(), list(), list()
        for curves in self.__curves_list:
            angles.append(curves.angle)
            lifts.append(curves.lift_avg)
            drags.append(curves.drag_avg)

        # Lifts plot
        plt.figure(figsize=figsize)
        plt.scatter(angles, lifts)
        plt.xlabel('Angle [deg]')
        plt.ylabel('Lift [N]')
        if show: plt.show()
        if save:
            if not path: path = os.path.join(OUTPUT_PATH, '_avgs_angle/lift_angle.jpg')
            try: os.makedirs(path)
            except: pass
            plt.savefig(path, bbox_inches='tight')

        # Drags plot
        plt.figure(figsize=figsize)
        plt.scatter(angles, drags)
        plt.xlabel('Angle [deg]')
        plt.ylabel('Drag [N]')
        if show: plt.show()
        if save:
            if not path: path = os.path.join(OUTPUT_PATH, '_avgs_angle/drag_angle.jpg')
            try: os.makedirs(path)
            except: pass
            plt.savefig(path, bbox_inches='tight')        