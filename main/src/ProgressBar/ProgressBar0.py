"""Progress bar with a known number of iterations (case of ClassificationCache) (and a known number of epochs)"""

import numpy as np
from rich.progress import Progress

from main.src.ProgressBar.AbstractProgressBar import AbstractProgressBar
from main.src.ProgressBar.IterationManager import IterationManager


class ProgressBar0( AbstractProgressBar):
    """Progress bar with a known number of iterations (case of ClassificationCache) (and a known number of epochs)

    Args:
        length: int, length of the dataset
        num_epochs: int, number of epochs
    """

    def __init__(self, iteration_manager: IterationManager):
        super(ProgressBar0, self).__init__()
        self._progress_bar = Progress(*self.columns)
        self.iteration_manager = iteration_manager
        self._progress_bar_task = self._progress_bar.add_task(
            "pb",
            name="[red]Progress",
            total=iteration_manager.total,
            status=0
        )

    def on_end(self,*args,**kwargs):
        """Update iteration progress bar"""

        self._progress_bar.update(self._progress_bar_task,
                                  advance=1,
                                  status=self.iteration_manager.next(),
                                  **kwargs
                                  )


    @property
    def progress_bar(self) -> Progress:
        return self._progress_bar
