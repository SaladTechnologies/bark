from transformers import AutoProcessor, AutoModel
from optimum.bettertransformer import BetterTransformer
import torch


def load(load_only=False):
    processor = AutoProcessor.from_pretrained("suno/bark")
    model = AutoModel.from_pretrained("suno/bark", torch_dtype=torch.float16)

    if not load_only:
        model.to("cuda")
        model = BetterTransformer.transform(model, keep_original_model=False)

    return processor, model
