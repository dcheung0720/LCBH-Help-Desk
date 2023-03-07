import pandas as pd
from sklearn import model_selection
from sklearn import neighbors
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.impute import SimpleImputer
import re



class responseGenerator():
    def __init__(self, dataset_file, n_neighbors):
        df = pd.read_csv(dataset_file)    #read csv of all past inquiry-response combinations
        df = df.dropna(subset=['Answer']) #remove pairs without a response (all rows in data have an inquiry)
        self.dataframe = df
        self.n_neighbors = n_neighbors
        self.fit_responses()
        
    def get_response(self,inquiry):
        trial = []
        trial.append(inquiry)
        trial_v = self.vectorizer.transform(trial)    #vectorizer inquiry
        #print("trial_v=",trial_v)
        #prediction = self.model.predict(trial_v)          #predict response
        #return prediction[0,0], prediction[0,1], prediction[0,2]
        predictions = self.model.kneighbors(trial_v)
        return self.clean_response(self.dataframe.iloc[predictions[1][0], :][["Answer","Answer Category","Inquiry"]].values.tolist())

    def clean_response(self, responses_list):
        #print("list: ", responses_list)
        for i in range(len(responses_list)):
            response_list = responses_list[i]
            text_answer = response_list[0]
            text_answer = text_answer.strip()
            possible_text = self.regex_cleaner(text_answer)
            if possible_text:
                text_answer = possible_text
            responses_list[i][0] = text_answer
        return responses_list

    def regex_cleaner(self, text):
        pattern = r'Question:.*Answer:\s*(.*)'
        match = re.search(pattern, text, re.DOTALL)
        if match:
            return match.group(1).strip()
        return None


    def add_data(self,inquiry,response,category):
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
        #self.dataframe = df
        
        


rG = responseGenerator(dataset_file= r"Help_Desk_Data_Cleaned_for_Category_Model_Mark_2.csv",n_neighbors=5)
print(rG.get_response(" My land lord is herrassing me with Textes and is giving me a hard time since I cought them in my apartment then they text me to try and cover there back but they text me 30 minutes after they left I never gave anyone permission to go into my apartment also the 5 windows in my apt have mold in them and do not close or work they slam open when the wind blows "))
#print(rG.get_response("I don't have enough money for rent this month"))

#rG.add_data("Hello there 123","This is an answer","Eviction")

#print(rG.get_response("Hello 123"))