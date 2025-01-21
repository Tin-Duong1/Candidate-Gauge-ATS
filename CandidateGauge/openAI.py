import openai
import re
from transformers import pipeline
# Set your API key
openai.api_key = ""
# Define a job description to compare against
# job_description = "We're looking for a software engineer with experience in Java and Python."

# Define a function to score a resume against the job description
# load the sentiment analysis pipeline
model_name = "distilbert-base-uncased-finetuned-sst-2-english"
model_revision = "af0f99b"
sentiment_pipeline = pipeline(
    "sentiment-analysis", model=model_name, revision=model_revision)


def score_resume(resume, job_description):
    prompt = f"Score this resume on a scale of 1 to 10 for how well it matches this job description:\n\n{job_description}\n\nResume: {resume[:500]}."
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=500,
        temperature=0.5
    )
    text = response["choices"][0]["text"].strip()
    score = re.findall(r'\d+', text)
    extract_sentiment = sentiment_pipeline(text)[0]
    sentiment_label, sentiment_score = extract_sentiment['label'], extract_sentiment['score']
    sentiment_score = round(sentiment_score, 2)
    if sentiment_label.lower() == "negative":
        sentiment_score = 1 - sentiment_score
    if not score:
        return -1, sentiment_label, sentiment_score
    else:
        return score[-1], sentiment_label, sentiment_score
