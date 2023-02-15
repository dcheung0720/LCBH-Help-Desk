#import torch
import pandas as pd
from sklearn import model_selection
from sklearn import neighbors
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.impute import SimpleImputer
from sklearn.metrics import pairwise_distances



# Idea: predict first 10 neighbors or so in order, then let user switch through them to choose

def my_distance(v1, v2):
    return pairwise_distances(v1, v2, metric="cosine")
    # If we are predicting category and response, we should add county and contact type
    # Only consider neighbors which are the same type (SMS or Email)
    # Favor? neighbors of same county


class responseGenerator():
    def __init__(self, dataset_file, n_neighbors):
        df = pd.read_csv(dataset_file)    #read csv of all past inquiry-response combinations
        self.dataframe = df.dropna(subset=['Answer']) #remove pairs without a response (all rows in data have an inquiry)
        self.dataframe = self.dataframe.dropna(subset=["Contact Type"])


        self.contact_types = ["Email","Text / SMS"]
        for c in self.contact_types:
            self.specific_dataframe[c] = self.dataframe.loc[self.dataframe['Contact Type'] == c]

        self.n_neighbors = n_neighbors
        
        self.fit_responses()
        
        
        
        


    def fit_responses(self):
        X = self.dataframe["Inquiry"]
        #self.X_text = X
        tfidf = TfidfVectorizer()
        X = tfidf.fit_transform(X)              #vectorize the text inquires for our model

        #X_both = self.dataframe[["Contact Type","Inquiry"]]
        tfidf_type = TfidfVectorizer()
        type_encoded = tfidf_type.fit_transform(self.dataframe["Contact Type"])
        #X_both = tfidf.fit_transform(X_both)
        #print(X)
        #X_both=list(zip(type_encoded,X))
        #print(X_both)
 
        Y = self.dataframe[["Answer","Answer Category","Inquiry"]]

        knn = neighbors.KNeighborsClassifier(n_neighbors=self.n_neighbors, metric="cosine")#my_distance)   #only one neighbor (find the closest past inquiry)
        # I think a lot can be done with the distance metric in order to get better results. For instance, we could add a fields... 
        # for categories, counties and create our own distance function that uses the cosine vector distance but then also makes sure the past response was the same category and county

        knn.fit(X,Y)                              #fit the model to the vectorized X data and text Y data
        self.model = knn
        self.vectorizer = tfidf                  #save our model and vectorizer for predictions
        self.contact_vectorizer = tfidf_type

        
        for c in self.contact_types:
            X_specific = self.specific_dataframe[c]["Inquiry"]
            X_specific = tfidf.fit_transform(X_specific)
            Y_specific = self.specific_dataframe[c][["Answer","Answer Category","Inquiry"]]
            knn = neighbors.KNeighborsClassifier(n_neighbors=self.n_neighbors, metric="cosine")
            knn.fit(X_specific,Y_specific)
            self.specific_model[c] = knn

    def get_response(self,inquiry,contact_type):
        trial = []
        trial.append(inquiry)
        trial_v = self.vectorizer.transform(trial)    #vectorizer inquiry

        #contact = []
        #contact.append(contact_type)
        #contact_v = self.contact_vectorizer.transform(contact)

        #print("trial_v=",trial_v)
        #input_v = list(zip(contact_v,trial_v))
        #prediction = self.model.predict(input_v)
        prediction = self.model.predict(trial_v)          #predict response
        return prediction[0,0], prediction[0,1], prediction[0,2]       #returns response, category, original inquiry
        #print(preds1)

    def add_data(self,inquiry,response,category,contact_type):
        if inquiry is None or response is None or category is None:
            print("WARNING: Inquiry, Answer, or Answer Category is null. Not adding data.")
            return
            
        new_row = {'Inquiry':[inquiry],
                    'Answer':[response],
                    'Answer Category':[category],
                    'Contact Type':[contact_type]}
        new_row_df = pd.DataFrame(new_row)
        self.dataframe = pd.concat([self.dataframe, new_row_df],ignore_index = True)
        self.specific_dataframe[contact_type] = pd.concat([self.specific_dataframe[contact_type], new_row_df],ignore_index = True)

        self.fit_responses()

        
    def get_response_contact_type(self,inquiry,contact_type):
        trial = []
        trial.append(inquiry)
        trial_v = self.vectorizer.transform(trial)    #vectorizer inquiry

        #contact = []
        #contact.append(contact_type)
        #contact_v = self.contact_vectorizer.transform(contact)

        #print("trial_v=",trial_v)
        #input_v = list(zip(contact_v,trial_v))
        #prediction = self.model.predict(input_v)
        prediction = self.specific_model[contact_type].predict(trial_v)          #predict response in given contact type
        return prediction[0,0], prediction[0,1], prediction[0,2]       #returns response, category, original inquiry

#tests


rG = responseGenerator(dataset_file= r"Help_Desk_Data_Cleaned_for_Category_Model_Mark_2.csv",n_neighbors=1)
print("First:",rG.get_response("Help, my landlord is trying to evict me!","Email")[2])
print("Second:",rG.get_response("I don't have enough money for rent this month","Text / SMS")[2])

print("Third:",rG.get_response("Hello 123","Text / SMS"))

rG.add_data("Hello there 123","This is an answer","Other","Email")

print("Fourth:",rG.get_response("Hello 123","Text / SMS"))

print("Fifth:",rG.get_response("Landlord is unresponsive","Email"))
