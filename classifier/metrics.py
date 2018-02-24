import numpy as np

from classifier.train import LOGGER


def compute_metrics(y, pred):
    """
    Compute perfomance metrics given the predicted labels and the true labels

    Args:
        y: True label vector
           (Type: np.ndarray)

        pred: Predicted label vector
              (Type: np.ndarray)

    Returns:
        metrics: Metrics dictionary
                 (Type: dict[str, *])
    """
    # Convert from one-hot to integer encoding if necessary
    if y.ndim == 2:
        y = np.argmax(y, axis=1)
    if pred.ndim == 2:
        pred = np.argmax(pred, axis=1)

    acc = (y == pred).mean()

    sum_class_acc = 0.0
    for class_idx in range(10):
        idxs = (y == class_idx)
        sum_class_acc += (y[idxs] == pred[idxs]).mean()

    ave_class_acc = sum_class_acc / 10

    return {
        'accuracy': acc,
        'average_class_accuracy': ave_class_acc
    }


def aggregate_metrics(fold_metrics):
    """
    Aggregate fold metrics using different stats

    Args:
        fold_metrics: List of fold metrics dictionaries
                      (Type: list[dict[str, *]])

    Returns:
        aggr_metrics: Statistics averaged across epochs
                      (Type: dict[str, dict[str,float]])
    """
    metric_keys = list(fold_metrics[0].keys())
    fold_metrics_list = {k: [fold[k] for fold in fold_metrics]
                         for k in metric_keys}
    aggr_metrics = {}

    for metric in metric_keys:
        metric_list = fold_metrics_list[metric]
        aggr_metrics[metric] = {
            'mean': np.mean(metric_list),
            'var': np.var(metric_list),
            'min': np.min(metric_list),
            '25_%ile': np.percentile(metric_list, 25),
            '75_%ile': np.percentile(metric_list, 75),
            'median': np.median(metric_list),
            'max': np.max(metric_list)
        }

    return aggr_metrics


def print_metrics(metrics, subset_name):
    """
    Print classifier metrics

    Args:
        metrics: Metrics dictionary
                 (Type: dict[str, *])
        subset_name: Name of subset to print
                     (Type: str)
    """
    LOGGER.info("Results metrics for {}".format(subset_name))
    LOGGER.info("=====================================================")
    for metric, metric_stats in metrics.items():
        LOGGER.info("* " + metric)
        for stat_name, stat_val in metric_stats.items():
            LOGGER.info("\t- {}: {}".format(stat_name, stat_val))
        LOGGER.info("\n")