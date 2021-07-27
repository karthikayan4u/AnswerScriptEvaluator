import os
import cv2
from pdf2image import convert_from_path
import pytesseract
from rouge import Rouge
import numpy
"""from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize"""

def calc(reference_answer, user_answer):

    """
    Cosine-Similarity
    # tokenization
    X_list = word_tokenize(admin_answer) 
    Y_list = word_tokenize(user_answer)
    
    # sw contains the list of stopwords
    sw = stopwords.words('english') 
    l1 =[];l2 =[]
    
    # remove stop words from the string
    X_set = {w for w in X_list if not w in sw} 
    Y_set = {w for w in Y_list if not w in sw}
    
    # form a set containing keywords of both strings 
    rvector = X_set.union(Y_set) 
    for w in rvector:
        if w in X_set: l1.append(1) # create a vector
        else: l1.append(0)
        if w in Y_set: l2.append(1)
        else: l2.append(0)
    c = 0
    
    # cosine formula 
    for i in range(len(rvector)):
            c+= l1[i]*l2[i]
    cosine = c / float((sum(l1)*sum(l2))**0.5)
    return cosine"""

    #Rouge based evaluation
    rouge = Rouge()
    scores = rouge.get_scores(user_answer.lower(), reference_answer.lower())[0]
    #75% importance to longest common subsequence matches and 25% to single word matches
    rouge_l = 0.75 * scores['rouge-l']['f']
    rouge_1 = 0.25 * scores['rouge-1']['f'] #f = f1 score
    score = rouge_l + rouge_1
    return score

def handle_uploaded_file(pdf, questions):
    with open(pdf.name, 'wb+') as destination:  
        for chunk in pdf.chunks():  
            destination.write(chunk)  
    pages = convert_from_path(pdf.name, 350)
    answers = {}
    cur_question = ''
    for i, page in enumerate(pages):
        image_name = "Page_" + str(i) + ".jpeg"  
        page.save(image_name, "JPEG")
        
        # load the original image
        img = cv2.imread(image_name)

        # convert the image to black and white for better OCR
        _,thresh1 = cv2.threshold(img,120,255,cv2.THRESH_BINARY)

        # pytesseract image to string to get results
        text = str(pytesseract.image_to_string(thresh1, config='--psm 6'))
        for question in questions:
            if question.question.lower() in text.lower():
                cur_question = question.question
                questions.remove(question)
                break
        processed_txt = text.replace(cur_question, '').strip()
        answers[cur_question] = answers.get(cur_question, '') + processed_txt
        os.remove("Page_" + str(i) + ".jpeg")
    os.remove(pdf.name)
    return answers
