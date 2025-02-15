from google import genai

title = ""
content = '''
'''

prompt = f'''you are a bot that helps frustrated users determine whether or not an article is clickbait bullshit. an article is defined as bullshit if it promises something in the title but does not actually talk about it or beats around the bush. You will be given a title and the content of the article and you will determine whether or not it's bullshit in terms of bullshit percentage. You will first give Consensus %, then a summary of the article, and then a final one line TLDR.

Example1)
Title: Bloodborne is coming to Playstation 5
Article: (only contains stuff about directors vaguely discussing the thought of porting it to playstation. no concrete proof of it actually happening)
Consensus: 70% Bullshit

Here's an actual article:
Title:  {title}

Content: {content}
'''

client = genai.Client(api_key="AIzaSyApK9yImqBxE6WOh470g6dxeEbaDkAd6kw")
response = client.models.generate_content(
    model="gemini-2.0-flash", contents=prompt
)

print(response.text)
