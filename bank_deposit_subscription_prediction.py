# -*- coding: utf-8 -*-
"""Bank Deposit Subscription Prediction

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1D28hWFjzaRbP97GzO9GEdxG4XEJ1FAOB
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, classification_report
import pickle

df_load = pd.read_csv('train.csv')
df_load

"""**Data Wrangling**"""

print(df_load.isnull().values.any())

df_load = df_load.fillna(df_load.median())

df_load['is_subscribed'].value_counts()

#Identifying Outliers
# identify outliers with standard deviation
from numpy.random import seed
from numpy.random import randn
from numpy import mean
from numpy import std
# seed the random number generator
seed(1)
# generate univariate observations
df_load = 5 * randn(10000) + 50
# calculate summary statistics
data_mean, data_std = mean(df_load), std(df_load)
# identify outliers
cut_off = data_std * 3
lower, upper = data_mean - cut_off, data_mean + cut_off
# identify outliers
outliers = [x for x in df_load if x < lower or x > upper]
print('Identified outliers: %d' % len(outliers))
# remove outliers
outliers_removed = [x for x in df_load if x >= lower and x <= upper]
print('Non-outlier observations: %d' % len(outliers_removed))

#Subscription percentage visualization
fig = plt.figure()
ax = fig.add_axes([0,0,1,1])
ax.axis('equal')
labels = [0,1]
subs = df_load.is_subscribed.value_counts()
ax.pie(subs, labels=labels, autopct='%.0f%%')
plt.show()

"""**Exploratory Data Analysis Variabel Numerik**"""

#Creating bin chart
numerical_features = ['age', 'duration', 'campaign', 'pdays', 'previous', 'emp.var.rate', 'euribor3m', 'nr.employed']
fig, ax = plt.subplots(2, 4, figsize=(15, 18))
#to plot 2 overlays of histogram per each numerical features, use a color of blue & orange respectively
df_load[df_load.is_subscribed==1][numerical_features].hist(bins=20, color='blue', alpha=0.5, ax=ax)
df_load[df_load.is_subscribed==0][numerical_features].hist(bins=20, color='orange', alpha=0.5, ax=ax)
plt.show()

"""**Exploratory Data Analysis Variabel Kategorik**"""

sns.set(style='darkgrid')
fig.ax = plt.subplots(figsize=(5, 6))
sns.countplot(data=df_load, x='job', hue='is_subscribed')

sns.countplot(data=df_load, x='marital', hue='is_subscribed')

sns.countplot(data=df_load, x='education', hue='is_subscribed')

sns.countplot(data=df_load, x='default', hue='is_subscribed')

sns.countplot(data=df_load, x='housing', hue='is_subscribed')

sns.countplot(data=df_load, x='loan', hue='is_subscribed')

sns.countplot(data=df_load, x='contact', hue='is_subscribed')

sns.countplot(data=df_load, x='month', hue='is_subscribed')

sns.countplot(data=df_load, x='day_of_week', hue='is_subscribed')

"""**Data Pre-Processing : Deleting Unnecessary Columns**"""

cleaned_df = df_load.drop(['poutcome'], axis=1)
print(cleaned_df)

"""**Data Pre-Processing : Encoding Data**"""

#Convert all the numeric columns to numerical data types
for column in cleaned_df.columns :
  if cleaned_df[column].dtype == np.number : continue
  #Perform encoding for each non-numeric column
  cleaned_df[column] = LabelEncoder().fit_transform(cleaned_df[column])

  print(cleaned_df.describe())

"""**Data Pre-Processing : Splitting Dataset**"""

#Predictor dan target
X = cleaned_df.drop('is_subscribed', axis=1)
y = cleaned_df['is_subscribed']

#Splitting train & test
x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

#Print according to the expected result
print('Jumlah baris & kolom dari x_train adalah :', x_train.shape, ', sedangkan jumlah baris & kolom dari y_train adalah:', y_train.shape)
print('Prosentase subscription di data training adalah:')
print(y_train.value_counts(normalize=True))
print('Jumlah baris & kolom dari x_test adalah:', x_test.shape, ', sedangkan jumlah baris & kolom dari y_test adalah:', y_test.shape)
print('Prosentase subscription di data testing adalah:')
print(y_test.value_counts(normalize=True))

"""**Modelling : Logistic Regression**"""

log_model = LogisticRegression().fit(x_train, y_train)
print('Model Regression yang terbentuk adalah : \n', log_model)

"""**Performansi Model Training : Menampilkan Metrics**"""

#Predict
y_train_pred = log_model.predict(x_train)

#Print Classification Report
print('Classification Report Training Model (Logistic Regression):')
print(classification_report(y_train, y_train_pred))

"""**Performansi Model Training : Menampilkan Plots**"""

#From confusion matrix as a Data Frame
confusion_matrix_df = pd.DataFrame((confusion_matrix(y_train, y_train_pred)), ('Not Subs', 'Subs'), ('Not Subs', 'Subs'))

#Plot confusion matrix
plt.figure()
heatmap = sns.heatmap(confusion_matrix_df, annot=True, annot_kws={'size':14}, fmt='d', cmap='YlGnBu')
heatmap.yaxis.set_ticklabels(heatmap.yaxis.get_ticklabels(), rotation=0, ha='right', fontsize=14)
heatmap.xaxis.set_ticklabels(heatmap.xaxis.get_ticklabels(), rotation=0, ha='right', fontsize=14)

plt.title('Confusion Matrix for Training Model \n (Logistic Regression)', fontsize=18, color='darkblue')
plt.ylabel('True Label', fontsize=14)
plt.xlabel('Predicted Label', fontsize=14)

plt.show()

"""**Performansi Data Testing : Menampilkan Metrics**"""

#Predict
y_test_pred = log_model.predict(x_test)

#Print Classification Report
print('Classification Report Testing Model (Logistic Regression):')
print(classification_report(y_test, y_test_pred))

"""**Performansi Data Testing : Menampilkan Plots**"""

#From confusion matrix as a Data Frame
confusion_matrix_df = pd.DataFrame((confusion_matrix(y_test, y_test_pred)), ('Not Subs', 'Subs'), ('Not Subs', 'Subs'))

#Plot confusion matrix
plt.figure()
heatmap = sns.heatmap(confusion_matrix_df, annot=True, annot_kws={'size':14}, fmt='d', cmap='YlGnBu')
heatmap.yaxis.set_ticklabels(heatmap.yaxis.get_ticklabels(), rotation=0, ha='right', fontsize=14)
heatmap.xaxis.set_ticklabels(heatmap.xaxis.get_ticklabels(), rotation=0, ha='right', fontsize=14)

plt.title('Confusion Matrix for Testing Model \n (Logistic Regression)', fontsize=18, color='darkblue')
plt.ylabel('True Label', fontsize=14)
plt.xlabel('Predicted Label', fontsize=14)

plt.show()

print(confusion_matrix(y_test, y_test_pred))

result = pd.DataFrame(y_test, columns=['id', 'is_subscribed'])
result

y_test.value_counts()

len(y_test_pred)

is_subscribed = pd.Series(y_test_pred)

print(len(x_test['id']))

"""📌Result nya di sini karena Random Forest & Gradient Boosting ternyata overfitting, jd nga kepake

📌Pengen gabungin y_test_pred sm x_test['id'] gan tp beda datatype gmn y helP 🙏🏻

**Modelling : Random Forest Classifier**
"""

rdf_model = RandomForestClassifier().fit(x_train, y_train)
print(rdf_model)

"""**Performansi Data Training : Menampilkan Metrics**"""

#Predict
y_train_pred = rdf_model.predict(x_train)

#Print Classification Report
print('Classification Report Training Model (Random Forest Classifier):')
print(classification_report(y_train, y_train_pred))

"""**Performansi Data Training : Menampilkan Plots**"""

#From confusion matrix as a Data Frame
confusion_matrix_df = pd.DataFrame((confusion_matrix(y_train, y_train_pred)), ('Not Subs', 'Subs'), ('Not Subs', 'Subs'))

#Plot confusion matrix
plt.figure()
heatmap = sns.heatmap(confusion_matrix_df, annot=True, annot_kws={'size':14}, fmt='d', cmap='YlGnBu')
heatmap.yaxis.set_ticklabels(heatmap.yaxis.get_ticklabels(), rotation=0, ha='right', fontsize=14)
heatmap.xaxis.set_ticklabels(heatmap.xaxis.get_ticklabels(), rotation=0, ha='right', fontsize=14)

plt.title('Confusion Matrix for Training Model \n (Random Forest Classifier)', fontsize=18, color='darkblue')
plt.ylabel('True Label', fontsize=14)
plt.xlabel('Predicted Label', fontsize=14)

plt.show()

"""**Performansi Data Testing : Menampilkan Metrics**"""

#Predict
y_test_pred = rdf_model.predict(x_test)

#Print Classification Report
print('Classification Report Testing Model (Random Forest Classifier):')
print(classification_report(y_test, y_test_pred))

"""**Performansi Data Testing : Menampilkan Plots**"""

#From confusion matrix as a Data Frame
confusion_matrix_df = pd.DataFrame((confusion_matrix(y_test, y_test_pred)), ('Not Subs', 'Subs'), ('Not Subs', 'Subs'))

#Plot confusion matrix
plt.figure()
heatmap = sns.heatmap(confusion_matrix_df, annot=True, annot_kws={'size':14}, fmt='d', cmap='YlGnBu')
heatmap.yaxis.set_ticklabels(heatmap.yaxis.get_ticklabels(), rotation=0, ha='right', fontsize=14)
heatmap.xaxis.set_ticklabels(heatmap.xaxis.get_ticklabels(), rotation=0, ha='right', fontsize=14)

plt.title('Confusion Matrix for Testing Model \n (Random Forest Classifier)', fontsize=18, color='darkblue')
plt.ylabel('True Label', fontsize=14)
plt.xlabel('Predicted Label', fontsize=14)

plt.show()

hasil_rfc = pd.DataFrame({
    'id' : final_test['id'],
    'is_subscribed' : pred
})

print(hasil_rfc.shape)

hasil_rfc['is_subscribed'].value_counts()

"""**Modelling : Gradient Boosting Classifier**"""



gbt_model = GradientBoostingClassifier().fit(x_train, y_train)
print(gbt_model)

"""**Performansi Data Training : Menampilkan Metrics**"""

#Predict
y_train_pred = gbt_model.predict(x_train)

#Print Classification Report
print('Classification Report Training Model (Gradient Boosting Classifier):')
print(classification_report(y_train, y_train_pred))

"""**Performansi Data Training : Menampilkan Plots**"""

#From confusion matrix as a Data Frame
confusion_matrix_df = pd.DataFrame((confusion_matrix(y_train, y_train_pred)), ('Not Subs', 'Subs'), ('Not Subs', 'Subs'))

#Plot confusion matrix
plt.figure()
heatmap = sns.heatmap(confusion_matrix_df, annot=True, annot_kws={'size':14}, fmt='d', cmap='YlGnBu')
heatmap.yaxis.set_ticklabels(heatmap.yaxis.get_ticklabels(), rotation=0, ha='right', fontsize=14)
heatmap.xaxis.set_ticklabels(heatmap.xaxis.get_ticklabels(), rotation=0, ha='right', fontsize=14)

plt.title('Confusion Matrix for Training Model \n (Gradient Boosting Classifier)', fontsize=18, color='darkblue')
plt.ylabel('True Label', fontsize=14)
plt.xlabel('Predicted Label', fontsize=14)

plt.show()

"""**Performansi Data Testing : Menampilkan Metrics**"""

#Predict
y_test_pred = gbt_model.predict(x_test)

#Print Classification Report
print('Classification Report Testing Model (Gradient Boosting Classifier):')
print(classification_report(y_test, y_test_pred))

"""**Performansi Data Testing : Menampilkan Plots**"""

#From confusion matrix as a Data Frame
confusion_matrix_df = pd.DataFrame((confusion_matrix(y_test, y_test_pred)), ('Not Subs', 'Subs'), ('Not Subs', 'Subs'))

#Plot confusion matrix
plt.figure()
heatmap = sns.heatmap(confusion_matrix_df, annot=True, annot_kws={'size':14}, fmt='d', cmap='YlGnBu')
heatmap.yaxis.set_ticklabels(heatmap.yaxis.get_ticklabels(), rotation=0, ha='right', fontsize=14)
heatmap.xaxis.set_ticklabels(heatmap.xaxis.get_ticklabels(), rotation=0, ha='right', fontsize=14)

plt.title('Confusion Matrix for Testing Model \n (Gradient Boosting Classifier)', fontsize=18, color='darkblue')
plt.ylabel('True Label', fontsize=14)
plt.xlabel('Predicted Label', fontsize=14)

plt.show()

"""**Conclusion**

*Logistic Regression Algorithm Accuracy* :
- train : 91%
- test : 91%
[Appropriate Fitting]

*Random Forest Classifier Algorithm Accuracy* :
- train : 100%
- test : 91%
[Overfitting]

*Gradient Boosting Classifier Algorithm Accuracy* :
- train : 93%
- test : 92%
[Overfitting]


"""