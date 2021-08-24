from abc import ABC, abstractmethod

from rich.progress import Progress, TextColumn, BarColumn, TimeElapsedColumn, TimeRemainingColumn, TaskID



class AbstractProgressBar:
    """Base class to build a progressbar"""

    def __init__(self):
        super().__init__()
        self.columns = [
            TextColumn("{task.fields[name]}", justify="right"),
            BarColumn(bar_width=None),
            "[progress.percentage]{task.percentage:>3.1f}%",
            "•",
            TextColumn("[bold blue]status: {task.fields[status]}", justify="right"),
            "•",
            TimeElapsedColumn(),
            "•",
            TimeRemainingColumn()
        ]


    @property
    def progress_bar(self) -> Progress:
        """Global progress bar object (with multiple progress bar potentially inside)"""
        raise NotImplementedError

    def __enter__(self, *args, **kwargs):
        """Context manager (with statement)"""
        return self.progress_bar.__enter__()

    def __exit__(self, *args, **kwargs):
        """Context manager (with statement)"""
        return self.progress_bar.__exit__(*args, **kwargs)

        