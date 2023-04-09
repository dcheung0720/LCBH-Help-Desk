import pandas as pd
from sklearn import model_selection
from sklearn import neighbors
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.impute import SimpleImputer
from mongo_import import get_df_from_mongodb, add_row_to_mongodb
import translation as translate
from responseCombine import combine_two_responses
from sklearn.metrics.pairwise import cosine_distances

CONNECTION_STRING = "mongodb+srv://jackdaenzer2024:eZUnYSdbNJuzvH9U@csx-lcbh.us3nupa.mongodb.net/csx-lcbh"


class responseGenerator():
    def __init__(self, n_neighbors):
        #df = pd.read_csv(dataset_file)    #read csv of all past inquiry-response combinations
        df = get_df_from_mongodb(CONNECTION_STRING)
        df = df.dropna(subset=['Answer']) #remove pairs without a response (all rows in data have an inquiry)
        self.dataframe = df
        self.n_neighbors = n_neighbors
        self.stop_words = ['hello','help','been', 'has', 'by', 'when', 'also', 'had', 'want', 'any', 'just', 'our', 'my', 'helpscout', 'about', 'are', 'if', 'issues', 'be', 'on', 've', 'don', 'is', 'she', 'did', 'can', 'it', 'since', 'like', 'to', 'them', 'us', 'no', 'previous', 'with', 'secure', 'back', 'me', 'net', 'do', 'without', 'told', 'an', 'and', 'there', 'have', 'from', 'legal', 'not', 'https', 'the', 'that', 'what', 'in', 'need', 'because', 'at', 'being', 'am', 'trying', 'will', 'rent', 'of', 'new', 'they', 'how', 'after', 'as', 'still', 'due', 'was', 'know', 'for', 'building', 'would', 'now', 'you', 'or', 'received', 'he', 'issue', 'get', 'we', 'but', 'all', 'so', 'this']

        self.fit_responses()
        
    def get_response(self,inquiry):
        trial = []
        trial.append(inquiry)
        trial_v = self.vectorizer.transform(trial)    #vectorizer inquiry
        predictions = self.model.kneighbors(trial_v)
        #print(predictions)
        inquiries = self.dataframe.iloc[predictions[1][0], :]["Inquiry"].values.tolist()
        categories = self.dataframe.iloc[predictions[1][0], :]["Answer Category"].values.tolist()
        responses = self.dataframe.iloc[predictions[1][0], :]["Answer"].values.tolist()
        #print(inquiries)
        dist_between = 0.9
        dist_diff = 0.15
        #for i in range(len(inquiries)-1):
        combined_response = None
        combined_category = None
        combined_inquiry = None
        i=0
        for j in range(1,len(inquiries)):
            if(self.inquiries_distance(inquiries[i],inquiries[j]) > dist_between and (abs(predictions[0][0][i]-predictions[0][0][j])<dist_diff)):
                print(inquiries[i],":::",inquiries[j],":::",self.inquiries_distance(inquiries[i],inquiries[j]),":::",predictions[0][0][i],predictions[0][0][j])
                combined_response = combine_two_responses(responses[i],responses[j])
                combined_category = categories[i] + " / " + categories[j]
                combined_inquiry = inquiries[i] + " / " + inquiries[j]
            if combined_response != None: break
        #print("trial_v=",trial_v)
        #prediction = self.model.predict(trial_v)          #predict response
        #return prediction[0,0], prediction[0,1], prediction[0,2]
       
        final_return = self.dataframe.iloc[predictions[1][0], :][["Answer","Answer Category","Inquiry"]].values.tolist()
        if combined_response == None:
            return final_return
        else:
            return self.clean_response([[combined_response,combined_category,combined_inquiry]] + final_return)


    def clean_response(self, responses_list):
        for i in range(len(responses_list)):
            response_list = responses_list[i]
            text_answer = response_list[0]
            text_answer = text_answer.strip()
            possible_text = self.regex_cleaner(text_answer)
            if possible_text:
                text_answer = possible_text
            
            text_answer = self.append_links(text_answer, self.link_finder(text_answer))
            responses_list[i][0] = text_answer
        return responses_list

    def regex_cleaner(self, text):
        pattern = r'Question:.*Answer:\s*(.*)'
        match = re.search(pattern, text, re.DOTALL)
        if match:
            return match.group(1).strip()
        return None

    def link_finder(self,text):
        text = text.replace("\n", " ")
        sentences = text.split(" ")
        links = []
        for sentence in sentences:
            if 'http' in sentence:
                index = sentence.find("http")
                sentence = sentence[index:]
                if sentence.endswith("."):
                    sentence = sentence[:-1]
                links.append(sentence)
        return links

    def append_links(self, text, links):
        text = text.rstrip()
        if len(links) == 0:
            if "Links:" in text:
                text = text.replace("Links:", "")
            return text
        
        if not "Links:" in text:
            text += "\n\nLinks: "
        else: 
            text = text.replace("Links:", "\n\nLinks: ")
        text += ", ".join(links)
        return text

    def add_data(self,inquiry,response,category):
        new_row = {'Inquiry':[inquiry],
                    'Answer':[response],
                    'Answer Category':[category]}
        # new_row_df = pd.DataFrame(new_row)
        # self.dataframe = pd.concat([self.dataframe, new_row_df],ignore_index = True)
        # self.fit_responses()
        add_row_to_mongodb(CONNECTION_STRING, new_row)
        

    def fit_responses(self):
        X = self.dataframe["Inquiry"]
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
        
    def inquiries_distance(self, inquiry1, inquiry2):
        i1 = self.vectorizer.transform([inquiry1])
        i2 = self.vectorizer.transform([inquiry2])
        return cosine_distances(i1,i2)
