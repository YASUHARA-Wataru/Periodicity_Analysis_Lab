from dataclasses import dataclass

@dataclass
class AnalysisConfig:
    window_size: int
    hop_size: int
    min_f0: float
    max_f0: float

    bayes_alpha: float = 0.7
    bayes_sigma: float = 0.1

    viterbi_beta: float = 10.0
    viterbi_sigma: float = 0.1