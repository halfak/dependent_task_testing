import random
import time


def score_many_models(model_names):
    """
    Generates score with random "processing" time
    """
    time.sleep(random.lognormvariate(-0.69, 1))  # Log normal processing time
    return {model_name: {"score": True} for model_name in model_names}


def score_model(model_scores, model_name):
    """
    Simply extracts score from pre-generated model map
    """
    return model_scores[model_name]
