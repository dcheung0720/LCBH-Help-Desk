import torch
import pandas as pd
from sklearn import model_selection
from sklearn import neighbors
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.impute import SimpleImputer



class responseGenerator():
    def __init__(self, dataset_file):
        df = pd.read_csv(dataset_file)    #read csv of all past inquiry-response combinations
        df = df.dropna(subset=['Answer']) #remove pairs without a response (all rows in data have an inquiry)

        X = df["Inquiry"]
        tfidf = TfidfVectorizer()
        X = tfidf.fit_transform(X)              #vectorize the text inquires for our model
 
        Y = df["Answer"]

        knn = neighbors.KNeighborsClassifier(n_neighbors=1, metric="cosine")     #only one neighbor (find the closest past inquiry)
        # I think a lot can be done with the distance metric in order to get better results. For instance, we could add a fields... 
        # for categories, counties and create our own distance function that uses the cosine vector distance but then also makes sure the past response was the same category and county


        knn.fit(X,Y)                              #fit the model to the vectorized X data and text Y data
        self.model = knn
        self.vectorizer = tfidf                  #save our model and vectorizer for predictions
        self.dataframe = df

    def get_response(self,inquiry):
        trial = []
        trial.append(inquiry)
        trial_v = self.vectorizer.transform(trial)    #vectorizer inquiry
        #print("trial_v=",trial_v)
        prediction = self.model.predict(trial_v)          #predict response
        return prediction
        #print(preds1)

    def add_data(self,inquiry,response):
        new_row = {'Inquiry':[inquiry],
                    'Answer':[response]}
        new_row_df = pd.DataFrame(new_row)
        self.dataframe = pd.concat([self.dataframe, new_row_df],ignore_index = True)

        X = self.dataframe["Inquiry"]
        tfidf = TfidfVectorizer()
        X = tfidf.fit_transform(X)              #vectorize the text inquires for our model
 
        Y = self.dataframe["Answer"]

        knn = neighbors.KNeighborsClassifier(n_neighbors=1, metric="cosine")     #only one neighbor (find the closest past inquiry)
        # I think a lot can be done with the distance metric in order to get better results. For instance, we could add a fields... 
        # for categories, counties and create our own distance function that uses the cosine vector distance but then also makes sure the past response was the same category and county


        knn.fit(X,Y)                              #fit the model to the vectorized X data and text Y data
        self.model = knn
        self.vectorizer = tfidf                  #save our model and vectorizer for predictions
        #print(self.dataframe)

        
        


rG = responseGenerator(dataset_file= r"Help_Desk_Data_Cleaned_for_Category_Model_Mark_2.csv")
print(rG.get_response("Help, my landlord is trying to evict me!"))
print(rG.get_response("I don't have enough money for rent this month"))

rG.add_data("Hello there 123","This is an answer")

print(rG.get_response("Hello 123"))
