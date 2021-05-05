from cleantext import clean
from main_config import options


f = open(options["raw_data_path"], "r", encoding="utf-8")
text = ""
for line in f:
    cleaned_line = clean(line,
                         fix_unicode=True,
                         to_ascii=True,
                         lower=False,
                         no_line_breaks=False,
                         no_urls=True,
                         no_emails=True,
                         no_phone_numbers=True,
                         no_numbers=False,
                         no_digits=False,
                         no_currency_symbols=True,
                         no_punct=False,
                         replace_with_punct="",
                         replace_with_url="<URL>",
                         replace_with_email="<EMAIL>",
                         replace_with_phone_number="<PHONE>",
                         replace_with_number="<NUMBER>",
                         replace_with_digit="0",
                         replace_with_currency_symbol="<CUR>",
                         lang="en"
                         )
    text = text + cleaned_line
f.close()
f = open(options["cleaned_data_path"], "w", encoding="utf-8")
f.write(text)
f.close()
