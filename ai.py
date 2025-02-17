from google import genai
import os
from dotenv import load_dotenv
from models import *

load_dotenv()
title = ""
content = '''
'''
gem_key = os.getenv("KEY")


def gen_report(title, content):
    prompt = f'''You are a bot that helps frustrated users determine whether or not an article is clickbait bullshit. an article is defined as bullshit if it promises something in the title but does not actually talk about it or beats around the bush. You will be given a title and the content of the article and you will determine whether or not it's bullshit in terms of bullshit percentage. You will first give Consensus percentage represented as an integer, then a breakdown represented as a string, and then a final one line TLDR represented as a string.

    Consensus meter:
    0-25%: Not Clickbait (Legit)
    26-74%: Slightly Clickbait (Mixed)
    75-100%: Clickbait (Bullshit)

    Example Input)
    Title: Bloodborne is coming to Playstation 5
    Article: (only contains stuff about directors vaguely discussing the thought of porting it to playstation. no concrete proof of it actually happening)    

    STRICTLY OUTPUT JSON ONLY AND FOLLOW THE EXAMPLE OUTPUT CLOSELY    

    Example Output1) 

    {{
        "percentage": 85,
        "explanation": "The title promises that Bloodborne is "officially returning," which strongly implies a new game, remaster, or re-release. However, the article is just about Bloodborne music being played at a PlayStation concert—nothing about the game itself coming back in any meaningful way. The content also tries to stretch this weak connection into speculation about a potential remaster, which isn't backed by any real evidence. Classic clickbait.": 
        "tldr": "Article provides no release date update, despite promising one in the title; pure clickbait"
    }}

    Example Output2) 
    {{
        "percentage": 60,
        "explanation": "The title is slightly clickbait because it confirms that Marvel Rivals devs are 'open' to a Switch 2 port and have dev kits. While technically true, the body of the article reveals that this openness is contingent on the Switch 2 providing 'great performance.' It is not a confirmation that the game is coming, just that they are considering it. There is no concrete announcement, just 'openness' and exploration.",
        "tldr": "Developers are 'open' to porting Marvel Rivals to Switch 2 if the console can handle it, but no port is confirmed."
    }}

    Here's an actual article:
    Title:  {title}

    Content: {content}    

    '''

    client = genai.Client(api_key=gem_key)
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=prompt,
        config={
        'response_mime_type': 'application/json',
        'response_schema': Output,
        },
    )

    return response

def gen_summary(content):
    sum_prompt = f'''Provide a comprehensive summary of the given article? The summary should cover all the key points and main ideas presented in the original text in an organised format, while also condensing the information into a concise and easy-to-understand format. Please ensure that the summary includes relevant details and examples that support the main ideas, while avoiding any unnecessary information or repetition. The length of the summary should be about 100 words, providing a clear and accurate overview without omitting any important information
    Article: {content}
    '''
    client = genai.Client(api_key=gem_key)
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=sum_prompt
    )

    # Extracting response text safely
    generated_summary = response.text if hasattr(response, "text") else str(response)
    return generated_summary
