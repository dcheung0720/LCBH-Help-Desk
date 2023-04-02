import pandas as pd
from sklearn import model_selection
from sklearn import neighbors
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.impute import SimpleImputer
from translation import inquiry_sort
from translation import *


class responseGenerator():
    def __init__(self, dataset_file, n_neighbors):
        df = pd.read_csv(dataset_file)    #read csv of all past inquiry-response combinations
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
        for i in self.dataframe.iloc[predictions[1][0], :]["Answer"]:
            print("HERE:",translate_text(i,'es'))
        return self.dataframe.iloc[predictions[1][0], :][["Answer","Answer Category","Inquiry"]].values.tolist()

    def add_data(self,inquiry,response,category):
        new_row = {'Inquiry':[inquiry],
                    'Answer':[response],
                    'Answer Category':[category]}
        new_row_df = pd.DataFrame(new_row)
        self.dataframe = pd.concat([self.dataframe, new_row_df],ignore_index = True)
        self.fit_responses()
        

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
        
        


rG = responseGenerator(dataset_file= r"Help_Desk_Data_Cleaned_for_Category_Model_Mark_2.csv",n_neighbors=5)
#print(rG.get_response("Help, my landlord is trying to evict me!"))
#print(rG.get_response("I don't have enough money for rent this month"))
print(rG.get_response("El pollos"))

#print(translate_text("\n\n\n            Gracias por contactarnos en Rentervention. Entiendo que recibió una\ncarta de desalojo de 5 días el 17 de marzo. Hay unos artículos con\ninformación sobre el proceso de desalojo [1] y cómo se puede\nresponder a un caso de desalojo [2]. Si recibió un aviso de 5 días\npor falta de pago del alquiler, es posible parar un caso de desalojo\nsi paga el monto total dentro del período de aviso de 5 días. Cuando\nel período de aviso de 5 días ha terminado, todavia se puede tratar\nde pagar un pago parcial de la deuda. Si el proprietario acepta el\npago parcial, el aviso se renuncia. Por lo tanto, el proprietario\nnecesita darle una carta de 5 días otra vez antes de presentar un\ncaso de desalojo. Sin embargo, el proprietario necesita aceptarlo.\nPara obtener más información, visite\nhttps://www.illinoislegalaid.org/es/legal-information/written-eviction-notices\n[3]. Si el propietario ya ha presentado un caso de desalojo, Cook\nCounty Legal Aid ofrece ayuda legal gratuita para los inquilinos en\nhttps://www.cookcountylegalaid.org/es/ [4].\nSi quiera solicitar asistencia de alquiler del estado de Illinois,\nllame a uno de los socios del Departamento de Servicios Humanos (DHS).\nHay una lista aqui:\nhttps://www.illinoisrentalassistance.com/providers#city-of-chicago_ID\n[5]. El Departamento de Servicios Familiares y de Apoyo de la ciudad\nde Chicago también tiene un programa de asistencia de alquiler\ndisponible, haga clic aquí para aplicar [6]\n\n\n\nLinks:\n', 'Eviction (Pre-Filing)', 'Recibí  una carta de desalojo de 5 dias el dia 17",'es'))

rG.add_data("Hello there 123","This is an answer","Eviction")

#print(rG.get_response("Hello 123"))
#print(rG.vectorizer.stop_words_)