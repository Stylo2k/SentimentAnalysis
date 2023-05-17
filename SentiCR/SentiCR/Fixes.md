
### All the problems below are probably due to the fact that I am using a different version of python than the one used in the original code

- changed the workbook library
- smote_model / SMOTE does not accept as many parameters as before ??
- smote_model.fit_sample(X_train, Y_train) is now smote_model.fit_resample(X_train, Y_train)
- python version  for i, j in dic.iteritems():
- the "string" in "expand_contractions" is now a byte string, so had to change that to be s.decode("utf-8")
