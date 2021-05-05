from sklearn.model_selection import train_test_split
from main_config import options


def split_test_train(data_path, test_path, train_path):
    f = open(data_path, "r", encoding="utf-8")
    data_nf = f.read().split('<EOS>')
    data = ["<BOS> " + x.split("<BOS>")[-1] + " <EOS> " for x in data_nf]
    f.close()
    print(str(len(data)) + " OF COMENTS")
    train, test = train_test_split(data, test_size=0.2)
    f = open(train_path, "w", encoding="utf-8")
    for tr in train:
        f.write(tr)
    f.close()
    f = open(test_path, "w", encoding="utf-8")
    for ts in test:
        f.write(ts)
    f.close()


def split_test_train_valid_lower(data_path, test_path, train_path, valid_path):
    f = open(data_path, "r", encoding="utf-8")
    data_nf = f.read().split('<eos>')
    data = ["<bos>" + x.split("<bos>")[-1] + "<eos> " for x in data_nf]
    f.close()
    print(str(len(data)) + " OF COMENTS")
    train, test = train_test_split(data, test_size=0.2)

    train, validate = train_test_split(data, test_size=0.25)

    f = open(train_path, "w", encoding="utf-8")
    for tr in train:
        f.write(tr)
    f.close()
    f = open(test_path, "w", encoding="utf-8")
    for ts in test:
        f.write(ts)
    f.close()
    f = open(valid_path, "w", encoding="utf-8")
    for vl in validate:
        f.write(vl)
    f.close()


def split_test_train_valid(data_path, test_path, train_path, valid_path):
    f = open(data_path, "r", encoding="utf-8")
    data_nf = f.read().split('<EOS>')
    data = ["<BOS>" + x.split("<BOS>")[-1] + "<EOS> " for x in data_nf]
    f.close()
    print(str(len(data)) + " OF COMENTS")
    train, test = train_test_split(data, test_size=0.2)

    train, validate = train_test_split(data, test_size=0.25)

    f = open(train_path, "w", encoding="utf-8")
    for tr in train:
        f.write(tr)
    f.close()
    f = open(test_path, "w", encoding="utf-8")
    for ts in test:
        f.write(ts)
    f.close()
    f = open(valid_path, "w", encoding="utf-8")
    for vl in validate:
        f.write(vl)
    f.close()


def main():
    if options["split_type"] == "ttvl":
        split_test_train_valid_lower(options["cleaned_data_path_no_dupes"],
                                     options["test_path"],
                                     options["train_path"],
                                     options["valid_path"], )
    if options["split_type"] == "ttv":
        split_test_train_valid(options["cleaned_data_path_no_dupes"],
                               options["test_path"],
                               options["train_path"],
                               options["valid_path"], )
    if options["split_type"] == "tt":
        split_test_train(options["cleaned_data_path_no_dupes"],
                         options["test_path"],
                         options["train_path"])


if __name__ == "__main__":
    main()
