from google import genai

title = ""
content = '''
'''

bs_prompt = f'''you are a bot that helps frustrated users determine whether or not an article is clickbait bullshit. an article is defined as bullshit if it promises something in the title but does not actually talk about it or beats around the bush. You will be given a title and the content of the article and you will determine whether or not it's bullshit in terms of bullshit percentage. You will give Consensus % at start, and then a one line TLDR in end, Do NOT say anything else.

Example1)
Title: Bloodborne is coming to Playstation 5
Article: (only contains stuff about directors vaguely discussing the thought of porting it to playstation. no concrete proof of it actually happening)
Consensus: 70% Bullshit

Here's an actual article:
Title:  {title}

Content: {content}
'''

client = genai.Client(api_key="AIzaSyApK9yImqBxE6WOh470g6dxeEbaDkAd6kw")
consensus = client.models.generate_content(
    model="gemini-2.0-flash", contents=bs_prompt
)

summary_prompt = f'''Provide a comprehensive summary of the given article? The summary should cover all the key points and main ideas presented in the original text in an organised format, while also condensing the information into a concise and easy-to-understand format. Please ensure that the summary includes relevant details and examples that support the main ideas, while avoiding any unnecessary information or repetition. The length of the summary should be about 80 words, providing a clear and accurate overview without omitting any important information
Article: {content}
'''

client = genai.Client(api_key="AIzaSyApK9yImqBxE6WOh470g6dxeEbaDkAd6kw")
summary = client.models.generate_content(
    model="gemini-2.0-flash", contents=summary_prompt
)

print(consensus.text)
print("Summary: " + summary.text)
