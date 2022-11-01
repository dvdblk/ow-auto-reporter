import json


def load_reasons(
    args, include: set = {"abusive_chat", "gameplay_sabotage", "inactivity", "spam"}
) -> dict:
    """Load reasons from a json file or return an empty dict

    Args:
        args: the argparse arguments
        include: set of reasons (keys) to include
    """
    reasons = json.load(open(args.reasons_fp))
    if include:
        reasons = dict(filter(lambda x: x[0] in include, reasons.items(),))

    return reasons
