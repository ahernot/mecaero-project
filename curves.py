import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
# from courbes_cx_cy import INPUT_PATH, OUTPUT_PATH

from preferences import *

REYNOLDS = 75000


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
        show = kwargs.get(True if save == False else False)

        # Lift plot
        plt.figure(figsize=figsize)
        plt.plot(self.time, self.lift, label=self.repr_short)
        plt.xlabel('Time [s]')
        plt.ylabel('Lift [N]')
        if show: plt.show()
        if save:
            if not path: path = os.path.join(OUTPUT_PATH, f'{self.repr_short}')
            try: os.makedirs(path)
            except: pass
            savepath = os.path.join(path, 'lift.jpg')
            plt.savefig(savepath, bbox_inches='tight')

        # Drag plot
        plt.figure(figsize=figsize)
        plt.plot(self.time, self.drag, label=self.repr_short)
        plt.xlabel('Time [s]')
        plt.ylabel('Drag [N]')
        if show: plt.show()
        if save:
            if not path: path = os.path.join(OUTPUT_PATH, f'{self.repr_short}')
            try: os.makedirs(path)
            except: pass
            savepath = os.path.join(path, 'drag.jpg')
            plt.savefig(savepath, bbox_inches='tight')    




class Data:

    def __init__ (self, reynolds: int):
        self.__reynolds = reynolds
        self.__curves_list = list()
        self.__curves_dict = dict()  # Curves, ordered by Reynolds number

        self.__airfoils = dict()

    def __repr__ (self):
        return f'Data for E={self.__reynolds}\n\nAirfoils:' + '\n\t'.join(list(self.__airfoils.keys()))


    def load (self, dirpath=INPUT_PATH):
        """
        Load data
        """
        with os.scandir(dirpath) as files:

            for file in files:
                if file.name in ('.DS_Store'): continue
                name, ext = os.path.splitext(file.name)

                # Retrieve dataframe
                df = pd.read_csv(file.path, sep='\t')

                name_split = name.split('_')
                for i, part in enumerate(name_split):
                    if part.lower() == 'naca':
                        airfoil = f'naca_{name_split[i+1]}'
                    elif part.lower() == 'i':
                        angle = float(name_split[i+1].replace('-', '.'))
                    elif part.lower()[0] == 'i':
                        angle = float(part[1:])

                # Fill dict of NACA profiles
                if not airfoil in self.__airfoils.keys(): self.__airfoils [airfoil] = dict()
                if not '__angles__' in self.__airfoils[airfoil].keys(): self.__airfoils [airfoil]['__angles__'] = list()
                self.__airfoils [airfoil][angle] = Curves(df, reynolds=self.__reynolds, angle=angle)
                self.__airfoils [airfoil]['__angles__'] .append(angle)
                
                # Add to self.__curves_list and self.__curves_dict
                # self.__curves_list .append(curves)
                # if reynolds not in self.__curves_dict.keys(): self.__curves_dict[reynolds] = dict()
                # self.__curves_dict [reynolds][angle] = curves


        # Generate ordered keys dictionaries
        self.__airfoils_list = list(self.__airfoils.keys())
        self.__airfoils_list.sort()
        for airfoil in self.__airfoils_list:
            self.__airfoils [airfoil]['__angles__'] .sort()
        


    def plot_all_individual (self, **kwargs):
        """
        Plot all the individual lift and drag curves
        """

        reynolds = REYNOLDS
        for angle in self.angles:
            curves = self.__curves_dict[reynolds][angle]
            curves.plot_individual(**kwargs)  # Individual plot


    def plot_comparison (self, **kwargs):

        # Unpack kwargs
        figsize = kwargs.get('figsize', (30, 10))
        save = kwargs.get('save', False)
        path = kwargs.get('path', None)
        if path: save = True
        show = kwargs.get(True if save == False else False)

        # Init plot
        fig, axs = plt.subplots(1, 2, figsize=figsize)

        # Plot for different airfoils
        for airfoil in self.__airfoils_list:

            angles_list = self.__airfoils[airfoil]['__angles__']
            lifts_list = [self.__airfoils[airfoil][angle].lift_avg for angle in angles_list]
            drags_list = [self.__airfoils[airfoil][angle].drag_avg for angle in angles_list]

            axs[0].plot(angles_list, lifts_list, label=airfoil)
            axs[1].plot(angles_list, drags_list, label=airfoil)
            axs[0].scatter(angles_list, lifts_list)
            axs[1].scatter(angles_list, drags_list)
        
        axs[0].set_xlabel('Angle [deg]')
        axs[0].set_ylabel('Lift [N]')
        axs[1].set_xlabel('Angle [deg]')
        axs[1].set_ylabel('Drag [N]')
        axs[0].legend(loc="upper right")
        axs[1].legend(loc="upper right")

        axs[0].set_title(f'Lifts for E={self.__reynolds}')
        axs[1].set_title(f'Drags for E={self.__reynolds}')

        if show: plt.show()
        if save:
            if not path: path = os.path.join(OUTPUT_PATH)
            try: os.makedirs(path)
            except: pass
            savepath = os.path.join(path, f'combined_reynolds-{self.__reynolds}.jpg')
            plt.savefig(savepath, bbox_inches='tight')



    # def plot_all_temporal (self, **kwargs):
    #     """
    #     Plot all the lifts (plot 1) and all the drags (plot 2) according to time, for a set Reynolds number
    #     """
    #     reynolds = REYNOLDS
    #     # if reynolds not in self.__curves_dict.keys(): raise ValueError('Wrong Reynolds number')

    #     # Unpack kwargs
    #     figsize = kwargs.get('figsize', (20, 10))
    #     save = kwargs.get('save', False)
    #     path = kwargs.get('path', None)
    #     if path: save = True
    #     show = kwargs.get(True if save == False else False)

    #     # Colormap
    #     colormap = cm.plasma
    #     colors_nb = min(colormap.N, self.angles_nb)
    #     mapcolors = [colormap(int(x*colormap.N/self.angles_nb)) for x in range(colors_nb)]

    #     # Lifts plot for each generated angle
    #     plt.figure(figsize=figsize)
    #     for i, angle in enumerate(self.angles):
    #         curves = self.__curves_dict[reynolds][angle]
    #         plt.plot(curves.time, curves.lift, label=curves.repr_short, c=mapcolors[i])
    #     plt.xlabel('Time [s]')
    #     plt.ylabel('Lift [N]')
    #     plt.legend()
    #     plt.title(f'Lifts for E={reynolds}')
    #     if show: plt.show()
    #     if save:
    #         if not path: path = os.path.join(OUTPUT_PATH, f'_combined-reynolds{reynolds}')
    #         try: os.makedirs(path)
    #         except: pass
    #         savepath = os.path.join(path, f'lifts-reynolds{reynolds}.jpg')
    #         plt.savefig(savepath, bbox_inches='tight')

    #     # Drags plot
    #     plt.figure(figsize=figsize)
    #     for i, angle in enumerate(self.angles):
    #         curves = self.__curves_dict[reynolds][angle]
    #         plt.plot(curves.time, curves.drag, label=curves.repr_short, c=mapcolors[i])
    #     plt.xlabel('Time [s]')
    #     plt.ylabel('Drag [N]')
    #     plt.legend()
    #     plt.title(f'Drags for E={reynolds}')
    #     if show: plt.show()
    #     if save:
    #         if not path: path = os.path.join(OUTPUT_PATH, f'_combined-reynolds{reynolds}')
    #         try: os.makedirs(path)
    #         except: pass
    #         savepath = os.path.join(path, f'drags-reynolds{reynolds}.jpg')
    #         plt.savefig(savepath, bbox_inches='tight')
   

    # def plot_avgs_angle (self, **kwargs):
    #     """
    #     Plot all the time-averaged lifts (plot 1) and drags (plot 2) according to angle
    #     """ # FOR A SET REYNOLDS NB?

    #     reynolds = REYNOLDS

    #     # Unpack kwargs
    #     figsize = kwargs.get('figsize', (20, 10))
    #     save = kwargs.get('save', False)
    #     path = kwargs.get('path', None)
    #     if path: save = True
    #     show = kwargs.get('show', True if save == False else False)

    #     # Unpack angles, lifts, drags
    #     angles, lifts, drags = list(), list(), list()
    #     for curves in self.__curves_list:
    #         angles.append(curves.angle)
    #         lifts.append(curves.lift_avg)
    #         drags.append(curves.drag_avg)

    #     # Lifts plot
    #     plt.figure(figsize=figsize)
    #     plt.scatter(angles, lifts)
    #     plt.xlabel('Angle [deg]')
    #     plt.ylabel('Lift [N]')
    #     plt.title(f'Time-averaged lifts according to angle for E={reynolds}')
    #     if show: plt.show()
    #     if save:
    #         if not path: path = os.path.join(OUTPUT_PATH, f'_avgs_angle-reynolds{reynolds}')
    #         try: os.makedirs(path)
    #         except: pass
    #         savepath = os.path.join(path, f'lift_angle-reynolds{reynolds}.jpg')
    #         plt.savefig(savepath, bbox_inches='tight')

    #     # Drags plot
    #     plt.figure(figsize=figsize)
    #     plt.scatter(angles, drags)
    #     plt.xlabel('Angle [deg]')
    #     plt.ylabel('Drag [N]')
    #     plt.title(f'Time-averaged drags according to angle for E={reynolds}')
    #     if show: plt.show()
    #     if save:
    #         if not path: path = os.path.join(OUTPUT_PATH, f'_avgs_angle-reynolds{reynolds}')
    #         try: os.makedirs(path)
    #         except: pass
    #         savepath = os.path.join(path, f'drag_angle-reynolds{reynolds}.jpg')
    #         plt.savefig(savepath, bbox_inches='tight')


"""
goal = plot lift/angle and drag/angle for different NACA profiles
goal = 
"""