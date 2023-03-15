from ray import serve
from fastapi import FastAPI
from typing import Dict, List
from sklearn.metrics import confusion_matrix

'''
    Classifiers
'''
import textblob_classifier.classifier as tb
import vader_classifier.classifier as vd
import stanza_classifier.classifier as sc
'''
    classes / models
'''
from classes import *

app = FastAPI()


@serve.deployment(route_prefix="/")
@serve.ingress(app)
class SentimentAnalysis:
    classifiers : Dict = {}
    
    def __init__(self, classifiers : Dict):
        self.classifiers = classifiers
    
    async def classify_sentence(self, classifier, sentence):
        return await classifier.classify.remote(sentence)

    async def classify_text(self, classifiers , text : str):
        results = []
        if not isinstance(classifiers, List):
            classifiers = [classifiers]
        
        for sentence in text:
            result = None
            if len(classifiers) > 1:
                result = await self.classify_mul_classifiers(classifiers, sentence)
            elif len(classifiers) == 1:
                result = await self.classify_sentence(classifiers[0], sentence)
                result = await result
            else:
                raise Exception("No classifiers provided")
            results.append(result)
        return results
    
    async def classify_mul_classifiers(self, classifiers, sentence):
            result = {}
            for classifier in classifiers:
                ref = await self.classify_sentence(classifier, sentence)
                name = self.get_classifier_name(self.classifiers, classifier)
                result[name] = await ref
            return result
    
    async def compare_text(self, classifiers, text : List[LabeledText]):
        results = []
        predicted = []
        expected = []

        for entry in text:
            sentence = entry['sentence']
            sentiment = entry['sentiment'].value.lower()
            comparison = {}
            for classifier in classifiers:
                ref = await self.classify_sentence(classifier, sentence)
                ref = await ref
                name = self.get_classifier_name(self.classifiers, classifier)
                sentiment_pre = ref.get('sentiment', '').lower()
                comparison[name] =  { 'expected_sentiment' : sentiment, 'predicted_sentiment' : sentiment_pre, 'correct_prediction': sentiment_pre == sentiment}
                
                expected.append(sentiment)
                predicted.append(sentiment_pre)

            results.append(comparison)
        confusion_matrix_result = confusion_matrix(expected, predicted, labels=['positive', 'negative', 'neutral'])
        results.append({'confusion_matrix' : confusion_matrix_result.tolist()})
        return results
            

    @app.post("/")
    async def classify_list_text(self, se_request: SeRequest):
        '''
            Classifies a list of sentences
        '''
        request = se_request.dict()
        classifier = request.get('classifier', None)
        text = request.get('text', None)
        classifier = self.classifiers.get(classifier, None)
        return await self.classify_text(classifier, text)


    @app.get("/")
    async def get_models(self):
        '''
            Returns a list of all available models
        '''
        names = []
        for classifier in self.classifiers:
            names.append(classifier.value)
        return names
    

    @app.post("/multiple")
    async def multiple_list_text(self, mul_request : MulRequest):
        '''
            Classifies a list of sentences with multiple classifiers
        '''
        request = mul_request.dict()
        classifiers = request.get('classifiers', None)
        text = request.get('text', None)
        results = {}
        ref_classifiers = []
        for classifier in classifiers:
            ref_classifiers.append(self.classifiers.get(classifier, None))
        
        results = await self.classify_text(ref_classifiers, text)

        return results

    @app.post('/compare')
    async def compare_list_text(self, cmp_request : CmpRequest):
        '''
            Compares a list of sentences with multiple classifiers
        '''
        request = cmp_request.dict()
        classifiers = request.get('classifiers', None)
        text : List[LabeledText] = request.get('text', None)
        results = {}
        ref_classifiers = []
        for classifier in classifiers:
            ref_classifiers.append(self.classifiers.get(classifier, None))
        
        results = await self.compare_text(ref_classifiers, text)
        return results
    
    def get_classifier_name(self, d, val):
        keys = [k for k, v in d.items() if v == val]
        if keys:
            return keys[0].value
        return None


sentiment_analysis = SentimentAnalysis.bind(
    {
        Classifiers.text_blob : tb.text_blob,
        Classifiers.vader : vd.vader,
        Classifiers.stanza : sc.stanza
    })