import re
import pandas as pd


#Takes in two examples of canned responses that want to combine, both should be from different categories
#For example, response1 can be an eviction response and response2 can be landlord retaliation
# In terms of actually combining the two responses, can parse to see if they're different topics, rather
# than relying directly on categories, as both 
def combine_two_responses(response1, response2):
    #Beginning: Thank you for using Rentervention and sorry for _____ and _______
    response1 = response1.strip() #cleans any leading spaces/paragraph breaks
    response2 = response2.strip()
    final_response = ""
    if "Thank you for using Rentervention." in response1:
            response1 = response1.replace("Thank you for using Rentervention.", "")
    if "Thank you for using Rentervention." in response2:
        response2 = response2.replace("Thank you for using Rentervention.", "")

    if "Thank you for contacting Rentervention." in response1:
        response1 = response1.replace("Thank you for contacting Rentervention.", "")
    if "Thank you for contacting Rentervention." in response2:
        response2 = response2.replace("Thank you for contacting Rentervention.", "")


    #Beginning: 
    final_response = final_response + "Thank you for using Rentervention. "
    topic_1 = finding_topic(response1)
    topic_2 = finding_topic(response2)


    #if both found topics
    if not topic_1 == None and not topic_2  == None:
        topic_string = ""
        
        #checking to see if topic starts with you or your:
        regex = re.compile(r'^(?:you|your|you\'re)\b', re.IGNORECASE)
        topic1Match = regex.match(topic_1)
        topic2Match = regex.match(topic_2)
        if topic1Match and topic2Match:
            topic_string = "I'm sorry to hear that " + topic_1 + ", and that " + topic_2 + "."
        elif topic1Match:
            topic_string = "I'm sorry to hear that " + topic_1 + ", and I understand that you have questions about " + topic_2 + " as well."
        elif topic2Match:
            topic_string = "I'm sorry to hear that " + topic_2 + ", and I understand that you have questions about " + topic_1 + " as well."
        else:
            topic_string = "I understand you have questions about " + topic_1 + ", and " + topic_2 + " as well."
        
        final_response = final_response + topic_string + "\n \n"

        final_response = final_response + "Regarding your first inquiry, I hope the following can help. "
        final_response = final_response + remove_topic_sentence(response1, topic_1) + "\n \n"

        final_response = final_response + "As for your other inquiry, hopefully the following information will help. "
        final_response = final_response + remove_topic_sentence(response2, topic_2) + "\n \n"
        

    elif topic_1 == None and topic_2 == None:

        final_response = final_response + "I understand you have more than one issue. \n \n"

        final_response = final_response + "Firstly, "
        final_response = final_response + response1 + "\n \n"

        final_response = final_response + "As for your other inquiry, I hope the following can help:"
        final_response = final_response + response2 + "."

    elif not topic_1 == None:
        regex = re.compile(r'^(?:you|your|you\'re)\b', re.IGNORECASE)
        topic1Match = regex.match(topic_1)
        if topic1Match:
            topic_string = "I'm sorry to hear that " + topic_1 + "."
        else:
            topic_string = "I understand you have questions about " + topic_1 + "."
        
        final_response = final_response + topic_string
        response1 = remove_topic_sentence(response1, topic_1)
        final_response = final_response + response1 + "\n \n"

        final_response = final_response + "As for your other inquiry, I hope the following can help: "
        final_response = final_response + response2 + "."

    elif not topic_2 == None:
        regex = re.compile(r'^(?:you|your|you\'re)\b', re.IGNORECASE)
        topic1Match = regex.match(topic_2)
        if topic1Match:
            topic_string = "I'm sorry to hear that " + topic_2 + "."
        else:
            topic_string = "I understand you have questions about " + topic_2 + "."
        
        final_response = final_response + topic_string
        response2 = remove_topic_sentence(response2, topic_2)
        final_response = final_response + response2 + "\n \n"

        final_response = final_response + "As for your other inquiry, I hope the following can help: "
        final_response = final_response + response1 

    return final_response


def remove_topic_sentence(string, phrase):
    # Split the string into sentences
    sentences = string.split(".")
    # Find the first sentence that contains the phrase
    for i, sentence in enumerate(sentences):
        if phrase in sentence:
            # Remove the first sentence that contains the phrase
            del sentences[i]
            break
    # Join the remaining sentences back into a string
    new_string = ".".join(sentences)
    return new_string

def finding_topic(response):

    pattern1 = r"sorry to hear that"
    phrase1 = "sorry to hear that"
    pattern2 = r"question about"
    phrase2 = "question about"
    pattern3 = r"i understand that"
    phrase3 = "I understand that"
    pattern4 = r"understand you're"
    phrase4 = "understand you're"

    match_one = matching(response, pattern1, phrase1)
    match_two = matching(response, pattern2, phrase2)
    match_three = matching(response, pattern3, phrase3)
    match_four = matching(response, pattern4, phrase4)

    topic = ""
    if not match_one == "" and not match_one == None:
        topic = match_one
    elif not match_two == "" and not match_two == None:
        topic = match_two
    elif not match_three == "" and not match_three == None:
        topic = match_three
    elif not match_four == "" and not match_four == None:
        topic = match_four
    
    
    else:
        pattern5 = r"(.*?[\.\?!]\s+)(.*?[\.\?!]\s+)(.*)"
        match5 = re.match(pattern5, response)
        if match5:
            second_sentence = match5.group(2)
            return second_sentence
    

    if not topic == "":
        return topic_cleaner(topic)


def topic_cleaner(topic):
    if not topic == "":
        pattern = r'[.,!;:]'  # Matches any of the characters inside the brackets
        match = re.search(pattern, topic)
        if match:
            index = match.end()
            substring = topic[:index-1]
            return substring
        else:
            return topic



def matching(text, pattern, phrase):
    sentences = re.split(r'[.!?]', text)  # split the text into sentences
    for sentence in sentences:
        if re.search(pattern, sentence, re.IGNORECASE):
            # found a sentence with pattern
            return re.sub(r'^\W+', '', sentence.split(phrase, 1)[1])
    return None
