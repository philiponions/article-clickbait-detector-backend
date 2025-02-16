from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
title = ""
content = '''
'''
gem_key = os.getenv("KEY")


def gen_report(title, content):
    prompt = f'''You are a bot that helps frustrated users determine whether or not an article is clickbait bullshit. an article is defined as bullshit if it promises something in the title but does not actually talk about it or beats around the bush. You will be given a title and the content of the article and you will determine whether or not it's bullshit in terms of bullshit percentage. You will first give Consensus %, then a breakdown, and then a final one line TLDR.

    Example1)
    Title: Bloodborne is coming to Playstation 5
    Article: (only contains stuff about directors vaguely discussing the thought of porting it to playstation. no concrete proof of it actually happening)
    Consensus: 70% Bullshit

    STRICTLY OUTPUT JSON ONLY AND FOLLOW THE EXAMPLE OUTPUT CLOSELY

    Example Output) 

    {{
        "percentage": 85,
        "explanation": "The title promises that Bloodborne is "officially returning," which strongly implies a new game, remaster, or re-release. However, the article is just about Bloodborne music being played at a PlayStation concert—nothing about the game itself coming back in any meaningful way. The content also tries to stretch this weak connection into speculation about a potential remaster, which isn't backed by any real evidence. Classic clickbait.": 
        "tldr": "Article provides no release date update, despite promising one in the title; pure clickbait"
    }}

    Here's an actual article:
    Title:  {title}

    Content: {content}

    '''

    client = genai.Client(api_key=gem_key)
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=prompt
    )

    # Extracting response text safely
    generated_report = response.text if hasattr(response, "text") else str(response)
    return generated_report

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
