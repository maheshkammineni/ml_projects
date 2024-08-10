import os
import sys
from dataclasses import dataclass
from catboost import catBoostRegresssor
from sklearn.ensemble import (
    AdaBoostRegressor, GradientBoostingRegressor,RandomForestRegressor
)

from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor

from src.exception import CustomException
from src.logger import logging

from src.utils import save_object

from dataclasses import dataclass, field
import os

@dataclass
class ModelTrainerConfig:
    trained_model_file_path: str = field(init=False)

    def __post_init__(self):
        self.trained_model_file_path = os.path.join("artifacts", "model.pkl")


class ModelTrainer:
