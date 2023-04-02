import pandas as pd
from sklearn import model_selection
from sklearn import neighbors
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.impute import SimpleImputer
from mongo_import import get_df_from_mongodb, add_row_to_mongodb

CONNECTION_STRING = "mongodb+srv://jackdaenzer2024:eZUnYSdbNJuzvH9U@csx-lcbh.us3nupa.mongodb.net/csx-lcbh"

class responseGenerator():
    def __init__(self, n_neighbors):
        df = get_df_from_mongodb(CONNECTION_STRING)
        #df = pd.read_csv(dataset_file)    #read csv of all past inquiry-response combinations
        df = df.dropna(subset=['Answer']) #remove pairs without a response (all rows in data have an inquiry)
        self.dataframe = df
        self.n_neighbors = n_neighbors
        self.stop_words = ['help','been', 'has', 'by', 'when', 'also', 'had', 'want', 'any', 'just', 'our', 'my', 'helpscout', 'about', 'are', 'if', 'issues', 'be', 'on', 've', 'don', 'is', 'she', 'did', 'can', 'it', 'since', 'like', 'to', 'them', 'us', 'no', 'previous', 'with', 'secure', 'back', 'me', 'net', 'do', 'without', 'told', 'an', 'and', 'there', 'have', 'from', 'legal', 'not', 'https', 'the', 'that', 'what', 'in', 'need', 'because', 'at', 'being', 'am', 'trying', 'will', 'rent', 'of', 'new', 'they', 'how', 'after', 'as', 'still', 'due', 'was', 'know', 'for', 'building', 'would', 'now', 'you', 'or', 'received', 'he', 'issue', 'get', 'we', 'but', 'all', 'so', 'this']

        self.fit_responses()
        
    def get_response(self,inquiry):
        trial = []
        trial.append(inquiry)
        trial_v = self.vectorizer.transform(trial)    #vectorizer inquiry
        #print("trial_v=",trial_v)
        #prediction = self.model.predict(trial_v)          #predict response
        #return prediction[0,0], prediction[0,1], prediction[0,2]
        predictions = self.model.kneighbors(trial_v)
        return self.dataframe.iloc[predictions[1][0], :][["Answer","Answer Category","Inquiry"]].values.tolist()

    def add_data(self,inquiry,response,category):
        new_row = {'Inquiry':inquiry,
                    'Answer':response,
                    'Answer Category':category}
        #new_row_df = pd.DataFrame(new_row)
        #self.dataframe = pd.concat([self.dataframe, new_row_df],ignore_index = True)
        add_row_to_mongodb(CONNECTION_STRING, new_row)   #This adds the given data point to the databse for future use

        #self.fit_responses()
        

    def fit_responses(self):
        X = self.dataframe["Inquiry"]
        #tfidf = TfidfVectorizer(max_df=0.1)
        tfidf = TfidfVectorizer(stop_words=self.stop_words)
        X = tfidf.fit_transform(X)              #vectorize the text inquires for our model
 
        #Y = df["Answer"]
        Y = self.dataframe[["Answer","Answer Category","Inquiry"]]   # Sample response, answer category, matched inquiry

        knn = neighbors.KNeighborsClassifier(n_neighbors=self.n_neighbors, metric="cosine")     #only one neighbor (find the closest past inquiry)
        # I think a lot can be done with the distance metric in order to get better results. For instance, we could add a fields... 
        # for categories, counties and create our own distance function that uses the cosine vector distance but then also makes sure the past response was the same category and county


        knn.fit(X,Y)                              #fit the model to the vectorized X data and text Y data
        self.model = knn
        self.vectorizer = tfidf                  #save our model and vectorizer for predictions
        #self.dataframe = df
        
        


rG = responseGenerator(n_neighbors=1)
#print(rG.get_response("Help, my landlord is trying to evict me!"))
#print(rG.get_response("I don't have enough money for rent this month"))

print(rG.get_response("Hello 123"))
#rG.add_data("Hello there 123","This is an answer","Eviction")
rG2 = responseGenerator(n_neighbors=1)
print(rG2.get_response("Hello 123"))

#print(rG.get_response("Hello 123"))
#print(rG.vectorizer.stop_words_)