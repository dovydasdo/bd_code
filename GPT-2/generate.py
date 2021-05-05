from transformers import GPT2Tokenizer
from transformers import AutoModelWithLMHead

model = AutoModelWithLMHead.from_pretrained("D:\\Bakalauro_darbas\\GPT-2\\GPT2-large")

pytorch_total_params = sum(p.numel() for p in model.parameters())

tokenizer = GPT2Tokenizer.from_pretrained('gpt2')

prompt = " "
inputs = tokenizer.encode(prompt, add_special_tokens=False, return_tensors="pt")
prompt_length = len(tokenizer.decode(inputs[0], skip_special_tokens=True, clean_up_tokenization_spaces=True))
outputs = model.generate(inputs, max_length=200, do_sample=True, top_p=1, top_k=60, output_attentions=True,
                         length_penalty=1.4, temperature=1, no_repeat_ngram_size=20, repetition_penalty=1.5)
generated = prompt + tokenizer.decode(outputs[0])[prompt_length:]

f = open("D:\\Bakalauro_darbas\\GPT-2\\bigger_comms\\test11.txt", "w", encoding="utf-8");

for comm in generated.split("<EOS>"):
    f.write(comm + "\n")

f.write(100 * '-' + "\n")

f.close()
