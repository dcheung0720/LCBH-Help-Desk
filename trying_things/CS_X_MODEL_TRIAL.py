import pandas as pd
from sklearn import model_selection
from sklearn import neighbors
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.impute import SimpleImputer
from translation import inquiry_sort



class responseGenerator():
    def __init__(self, dataset_file, n_neighbors):
        df = pd.read_csv(dataset_file)    #read csv of all past inquiry-response combinations
        df = df.dropna(subset=['Answer']) #remove pairs without a response (all rows in data have an inquiry)
        self.dataframe = df
        self.specific_dataframe = {"Email": [],
                                   "Text / SMS": []}
        self.contact_types = ["Email","Text / SMS"]
        for c in self.contact_types:
            self.specific_dataframe[c] = self.dataframe.loc[self.dataframe["Contact Type"]==c]
        
        self.n_neighbors = n_neighbors
        self.fit_responses()
        
    def get_response(self,inquiry,contact_type):
        
        trial = []
        trial.append(inquiry)
        trial_v = self.vectorizer.transform(trial)    #vectorizer inquiry
            #print("trial_v=",trial_v)
            #prediction = self.model.predict(trial_v)          #predict response
            #return prediction[0,0], prediction[0,1], prediction[0,2]
        if contact_type == None:
            predictions = self.model.kneighbors(trial_v)
            return self.dataframe.iloc[predictions[1][0], :][["Answer","Answer Category","Inquiry"]].values.tolist()
        else:
            predictions = self.specific_model[contact_type].kneighbors(trial_v)
            return self.specific_dataframe[contact_type].iloc[predictions[1][0], :][["Answer","Answer Category","Inquiry"]].values.tolist()


    def add_data(self,inquiry,response,category):    #THIS IS BEHIND
        new_row = {'Inquiry':[inquiry],
                    'Answer':[response],
                    'Answer Category':[category]}
        new_row_df = pd.DataFrame(new_row)
        self.dataframe = pd.concat([self.dataframe, new_row_df],ignore_index = True)
        self.fit_responses()
        

    def fit_responses(self):
        X = self.dataframe["Inquiry"]
        tfidf = TfidfVectorizer()
        X = tfidf.fit_transform(X)              #vectorize the text inquires for our model
 
        #Y = df["Answer"]
        Y = self.dataframe[["Answer","Answer Category","Inquiry"]]   # Sample response, answer category, matched inquiry

        knn = neighbors.KNeighborsClassifier(n_neighbors=self.n_neighbors, metric="cosine")     #only one neighbor (find the closest past inquiry)
        # I think a lot can be done with the distance metric in order to get better results. For instance, we could add a fields... 
        # for categories, counties and create our own distance function that uses the cosine vector distance but then also makes sure the past response was the same category and county


        knn.fit(X,Y)                              #fit the model to the vectorized X data and text Y data
        self.model = knn
        self.vectorizer = tfidf                  #save our model and vectorizer for predictions

        self.specific_model = {"Email": [],
                                "Text / SMS": []}
        for c in self.contact_types:
            X = self.specific_dataframe[c]["Inquiry"]
            X = tfidf.transform(X)
            Y = self.specific_dataframe[c][["Answer","Answer Category","Inquiry"]]
            knn = neighbors.KNeighborsClassifier(n_neighbors=self.n_neighbors, metric="cosine")
            knn.fit(X,Y)
            self.specific_model[c] = knn
        #self.dataframe = df
        
        


rG = responseGenerator(dataset_file= r"Help_Desk_Data_Cleaned_for_Category_Model_Mark_2.csv",n_neighbors=1)
print("Either:",rG.get_response("Help, my landlord is trying to evict me!",None)[0][0])
print("Text:",rG.get_response("Help, my landlord is trying to evict me!","Text / SMS")[0][0])
print("Email:",rG.get_response("Help, my landlord is trying to evict me!","Email")[0][0])
#print(rG.get_response("I don't have enough money for rent this month"))

#rG.add_data("Hello there 123","This is an answer","Eviction")

#print(rG.get_response("Hello 123"))
