from typing import List


def read_lines(filepath: str) -> List[str]:
    """Read text file

    Args:
        filepath: path of the test file where each line is split by '\n'
    Returns:
        lines: list of lines
    """
    with open(filepath, "r", encoding="utf-8") as f:
        lines = [line.rstrip("\n") for line in f]
    return lines


def get_configs(langpair: str) -> DictConfig:
    """Get all configurations regarding model training

    Args:
        langpair: language pair to train transformer
    Returns:
        configs: a single configuration that merged dataset, tokenizer, and model configurations
    """
    root_dir = Path(__file__).parent.parent
    dataset_config_dir = root_dir / "configs" / "dataset"
    tokenizer_config_dir = root_dir / "configs" / "tokenizer"
    model_config_dir = root_dir / "configs" / "model"

    configs = OmegaConf.create()

    model_config_path = model_config_dir / "transformers.yaml"
    model_config = OmegaConf.load(model_config_path)

    if langpair in ["de-en", "en-de", "deen", "ende"]:
        langpair = "deen"
        dataset_config_path = dataset_config_dir / f"wmt14.{langpair}.yaml"
        tokenizer_config_path = tokenizer_config_dir / f"sentencepiece_bpe_wmt14_{langpair}.yaml"
    # TODO: add en-fr
    #  elif langpair in ["en-fr", "fr-en", "enfr", "fren"]:
        #  langpair = "enfr"
        #  dataset_config_path = dataset_config_dir / f"wmt14.{langpair}.yaml"
        #  tokenizer_config_path = tokenizer_config_dir / f"sentencepiece_bpe_wmt14_{langpair}.yaml"
    else:
        raise NotImplementedError(
            f'{langpair} is not supported, since Hephaestus project aims to reproduce "Attention is all you need".'
        )

    dataset_config = OmegaConf.load(dataset_config_path)
    tokenizer_config = OmegaConf.load(tokenizer_config_path)
    tokenizer_config.tokenizer_vocab = root_dir / "tokenizer" / tokenizer_config.tokenizer_name + '-vocab.json'
    tokenizer_config.tokenizer_merges = root_dir / "tokenizer" / tokenizer_config.tokenizer_name + '-merges.txt'

    configs.update(dataset=dataset_config, tokenizer=tokenizer_config, model=model_config)
    return configs
