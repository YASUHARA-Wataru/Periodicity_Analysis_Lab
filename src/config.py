from dataclasses import dataclass

@dataclass
class AnalysisConfig:
    window_size: int
    hop_size: int
    min_f0: float
    max_f0: float