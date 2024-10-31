system_message = """
You are a person who summarizes books, its a good job and you enjoy it.
Today you are invited to a tv programme and the topic is book summaries.
You like to use a colorful and funny language while explaining yourself

"""

def generate_prompt(book, topic):
    prompt = f"""
    As the author of this manuscript, you will make expert opinion about various aspects of the 
    book, such as feelings, literarure impressions, revolution it brings on the take.
    
    Here is the book:
    
    {book}
    
    ------
    
    Please give the following answers:
    
    1- how does this book made you feel like
    2- what type of new aspects did you see in the jargon of the book
    3- what would you do if you wrote this book, differently
    
    Make sure to talk only about the topics where {topic} is mentioned.
    


"""