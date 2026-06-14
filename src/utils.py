import logging
import os
import random
import sys

import numpy as np
import torch

logger = logging.getLogger(__name__)


def set_seed(seed):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)

    if torch.cuda.is_available():
        torch.cuda.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False


def setup_logging(verbose: bool = False) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)-8s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
        stream=sys.stderr,
        force=True,
    )

    # Patch transformers warning_once / info_once to avoid TypeError formatting traceback
    def safe_warning_once(self, *args, **kwargs):
        if len(args) > 1 and isinstance(args[1], type) and issubclass(args[1], Warning):
            args = (args[0],)
        try:
            self.warning(*args, **kwargs)
        except TypeError:
            if args:
                self.warning(args[0])

    def safe_info_once(self, *args, **kwargs):
        if len(args) > 1 and isinstance(args[1], type) and issubclass(args[1], Warning):
            args = (args[0],)
        try:
            self.info(*args, **kwargs)
        except TypeError:
            if args:
                self.info(args[0])

    logging.Logger.warning_once = safe_warning_once
    logging.Logger.info_once = safe_info_once

    # Keep normal runs readable. These libraries can emit one line per HTTP
    # probe or model/cache file, which hides the actual indexing/eval status.
    noisy_loggers = (
        "chromadb",
        "filelock",
        "httpx",
        "httpcore",
        "huggingface_hub",
        "openai",
        "sentence_transformers",
        "tokenizers",
        "transformers",
        "urllib3",
    )
    for lib in noisy_loggers:
        logging.getLogger(lib).setLevel(logging.WARNING)

    if not verbose:
        os.environ.setdefault("HF_HUB_DISABLE_PROGRESS_BARS", "1")
