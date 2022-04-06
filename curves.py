import os
import pandas as pd
from courbes_cx_cy import OUTPUT_PATH

from preferences import *


class Curves: # drag/lift curves according to time, angle, reynolds

    def __init__ (self, df: pd.DataFrame, reynolds: float, angle: float):
        self.df = df

        self.time = df['Temps']
        self.drag = df['Cx0']
        self.lift = df['Cy0']
        self.reynolds = reynolds
        self.angle = angle

        self.repr_short = f'plots-reynolds{int(self.reynolds)}-angle{self.angle}'

    def __repr__ (self):
        return self.repr_short

    def plot (self, **kwargs):
        save = kwargs.get('save', False)
        path = kwargs.get('path', os.path.join(OUTPUT_PATH, self.repr_short))
        show = kwargs.get('show', True)

        # plot
        # show

        if save:
            try: os.makedirs(path)
            except: pass
            # savefig




class Data:

    def __init__ (self):
        self.curves = list()
        self.curves_reynolds = dict()  # Curves, ordered by Reynolds number

    def load (self, dirpath=INPUT_FOLDER):
        with os.scandir(dirpath) as files: # add a loop for reynolds folders

            for file in files:
                name, ext = os.path.splitext(file.name)
                df = pd.read_csv(file.path, sep='\t')

                # Retrieve information
                reynolds = 50000
                angle = float(name.split('_')[-1])

                # Generate Curves object
                curves = Curves(df, reynolds=reynolds, angle=angle)
                
                # Add to self.curves and self.curves_reynolds
                self.curves .append(curves)
                if reynolds not in self.curves_reynolds.keys: self.curves_reynolds[reynolds] = dict()
                self.curves_reynolds [reynolds][angle] = curves

