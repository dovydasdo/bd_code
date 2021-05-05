from tokenizers import ByteLevelBPETokenizer

tokenizer = ByteLevelBPETokenizer()

tokenizer.train(files=["D:\\Bakalauro_darbas\\Data\\full_data.txt"], vocab_size=52_000, min_frequency=2, special_tokens=[
    "<BOS>",
    "<EOS>",
    "<URL>",
    "<EMAIL>",
    "<PHONE>"
])

tokenizer.save_model("D:\\Bakalauro_darbas\\GPT-2\\tokenizer", "full_data")