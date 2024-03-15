from __future__ import annotations

from typing import List
from abc import ABC, ABCMeta, abstractmethod
from edsl.jobs.Jobs import Jobs
from edsl.results import Results

# used for typing
from edsl.jobs.buckets import BucketCollection
from edsl.jobs.Interview import Interview

class RegisterJobsRunnerMeta(ABCMeta):
    """Registers JobRunner classes."""
    _registry: dict[str, JobsRunner] = {}  # Initialize the registry as a dictionary

    def __init__(cls, name, bases, dct):
        super(RegisterJobsRunnerMeta, cls).__init__(name, bases, dct)
        if name != "JobsRunner":
            RegisterJobsRunnerMeta._registry[name] = cls

    @classmethod
    def get_registered_classes(cls) -> dict[str, JobsRunner]:
        """Return the JobsRunner registry."""
        return cls._registry

    @classmethod
    def lookup(cls):
        d = {}
        for classname, cls in cls._registry.items():
            if hasattr(cls, "runner_name"):
                d[cls.runner_name] = cls
            else:
                raise Exception(
                    f"Class {classname} does not have a runner_name attribute."
                )
        return d


class JobsRunner(ABC, metaclass=RegisterJobsRunnerMeta):
    """ABC for JobRunners, which take in a job, conduct interviews, and return their results."""

    def __init__(self, jobs: Jobs):
        self.jobs = jobs
        self.interviews: List['Interview'] = jobs.interviews()
        self.bucket_collection: 'BucketCollection' = jobs.bucket_collection
        self.total_interviews: List['Interview'] = []
        
    @abstractmethod
    def run(
        self,
        n: int = 1,
        debug: bool = False,
        verbose: bool = False,
        progress_bar: bool = True,
    ) -> Results:  # pragma: no cover
        """
        Runs the job: conducts Interviews and returns their results.

        - `n`: how many times to run each interview
        - `debug`: prints debug messages
        - `verbose`: prints messages
        - `progress_bar`: shows a progress bar
        """
        raise NotImplementedError
