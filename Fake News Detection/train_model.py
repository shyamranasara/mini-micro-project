import pandas as pd
import numpy as np
import joblib
import os
import re
import string
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

def clean_text(text):
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r'\[.*?\]', '', text)
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    text = re.sub(r'<.*?>+', '', text)
    text = re.sub(r'[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub(r'\n', '', text)
    text = re.sub(r'\w*\d\w*', '', text)
    return text.strip()

def create_synthetic_benchmark_dataset():
    """Create a high quality benchmark dataset for initial training."""
    fake_samples = [
        "BREAKING: Aliens landed in White House and signed peace treaty with the president today! Experts stunned as flying saucers land in broad daylight.",
        "SHOCKING SECRET: Drinking boiled lemon peel water cures all forms of cancer in 24 hours! Big Pharma does not want you to know this secret remedy.",
        "Scientific study claims eating chocolate 10 times a day makes you live until 200 years old. Doctors are baffled by this simple trick.",
        "Government secretly placing mind-control microchips in everyday drinking water to monitor citizen thoughts nationwide.",
        "Miracle pill discovered that burns 50 pounds of fat overnight without exercise or diet changes! Order now before supply runs out.",
        "Leaked secret documents reveal moon landing was filmed in a Hollywood basement directed by famous film makers.",
        "Celebrity secretly replaced by clone after mysterious disappearance in private island, fans notice strange behaviors.",
        "BREAKING: Millionaire hands out $10000 bills on streets to anyone who re-tweets this viral post within 10 minutes!",
        "Scientists discover secret portal to parallel dimension in South Pole ice cave, researchers enter another universe.",
        "Ancient pyramid found under local city park contains alien technology that generates free infinite electricity.",
        "5G towers cause instant magnetic field changes that make spoons stick to your arms, viral video claims.",
        "Secret formula revealed: mixing vinegar and baking soda grants immunity to all viruses forever.",
        "NASA announces Sun will turn green for three days next month due to rare solar energy alignment.",
        "Billionaire buying entire country to convert it into giant amusement park for pets.",
        "World leaders secretly meeting in underground bunker to discuss artificial cloud formation for weather control.",
        "Drinking 5 liters of sea water per day rejuvenates skin by 30 years in just one week according to viral blog.",
        "Scientists invent telepathy headset that reads any person's mind from 50 feet away.",
        "Unbelievable: Local cat elected as city mayor after landslide victory in municipal elections.",
        "Hidden underground city found beneath Sahara desert housing thousands of ancient humanoids.",
        "Exposed: Drinking tap water turns your eyes blue over time according to unverified online report."
    ]
    
    real_samples = [
        "The Federal Reserve announced an interest rate adjustment following its quarterly monetary policy review meeting today.",
        "Researchers at Johns Hopkins University published new peer-reviewed findings regarding cardiovascular health indicators in medical journal.",
        "The Supreme Court heard oral arguments today regarding national environmental regulatory frameworks and administrative law limits.",
        "Global stock markets experienced moderate gains as technology sector earnings surpassed quarterly analyst expectations.",
        "The World Health Organization issued updated guidance on seasonal influenza vaccination recommended for vulnerable populations.",
        "Engineers at NASA successfully completed ground tests for the next-generation space exploration propulsion system.",
        "European Union negotiators reached a preliminary agreement on renewable energy infrastructure funding across member states.",
        "Local government officials approved the annual municipal budget allocated for public school renovations and road repair projects.",
        "Astronomers using the James Webb Space Telescope observed atmospheric compositions of exoplanets in distant star systems.",
        "The Department of Transportation launched a initiative to modernize rail corridors and enhance intercity passenger rail speed.",
        "Medical researchers report progress in Phase 3 clinical trials evaluating targeted antibody therapies for autoimmune diseases.",
        "The international climate conference concluded with participating nations committing to target reduction goals in carbon emissions.",
        "University study demonstrates positive correlation between regular physical aerobic activity and cognitive function retention in adults.",
        "The central bank published economic growth projections estimating moderate GDP growth over the upcoming fiscal year.",
        "City council members voted unanimously to expand public parks and urban green spaces in downtown residential sectors.",
        "Tech company announces open source release of security tools designed to patch critical infrastructure vulnerabilities.",
        "Meteorologists forecast seasonal rainfall patterns adhering to historical averages across agricultural heartland regions.",
        "The Ministry of Health announced expanded access to preventative care clinics in rural communities across the country.",
        "Automotive manufacturer expands electric vehicle assembly line creating new engineering and technical jobs.",
        "Scientific publication outlines advancements in solar cell energy conversion efficiency using perovskite materials."
    ]
    
    data = []
    for text in fake_samples:
        data.append({'text': text, 'label': 1}) # 1 = Fake
    for text in real_samples:
        data.append({'text': text, 'label': 0}) # 0 = Real
        
    return pd.DataFrame(data)

def train_and_save():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    df = create_synthetic_benchmark_dataset()
    
    df['clean_text'] = df['text'].apply(clean_text)
    
    vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1, 2))
    X = vectorizer.fit_transform(df['clean_text'])
    y = df['label']
    
    model = LogisticRegression(C=1.0, random_state=42)
    model.fit(X, y)
    
    y_pred = model.predict(X)
    print("Fake News Model Accuracy on Benchmark:", accuracy_score(y, y_pred))
    
    joblib.dump(model, os.path.join(script_dir, 'model.pkl'))
    joblib.dump(vectorizer, os.path.join(script_dir, 'vectorizer.pkl'))
    print("Fake News Model & Vectorizer saved successfully!")

if __name__ == '__main__':
    train_and_save()
