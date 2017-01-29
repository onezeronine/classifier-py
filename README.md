# classifier-py

Runs on Python 3.6. This programs classifies gender based on the first name. Uses Multinomial Naive Bayes.

You can check the dataset on __names.csv__ file.

If you want to get random results, uncomment the `random.shuffle(r)` in `extractData`.

How to run on interactive python shell.

```sh
$ python -i main.py

>>> classify('mary')
f
>>> classify('john')
m
```

To get the evaluation result:
```sh
$ python -i main.py

>>> test()
Precision(f) => 0.8554216867469879
Recall(f) => 0.4226190476190476
F(f) => 0.5657370517928286
Precision(m) => 0.5907172995780591
Recall(m) => 0.9210526315789473
F(m) => 0.7197943444730077
```
