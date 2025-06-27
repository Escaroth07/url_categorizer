def combine_predictions(content_pred, content_conf):
    # Always accept the ML model's best guess, regardless of confidence
    return content_pred, content_conf
