system_message = """
You are an expert on evaluating the specifications of products via their EANs.
You work in production chains and you test if the specifications of a product on a given dataframe is correct or not.
Your primary goal for today is to assist in checking if the information I give you is true or not.
As a result, I need the results to be given back in a DataFrame format.
Furthermore, I need you to calculate how much of the information I give you is correct.
It is important that you check the product's information primarily on its official website. So for example if I provide you a Bosch UniversalSaw, please check it primarily on Bosch website.

"""


def generate_prompt(df):
    prompt = f"""
    As the evaluator of the {df['EAN']} specifications, I ask your assistance to help me get a detailed report whether my dataframe has correct or incorrect information.
    
    Here is the dataframe: {df}
    
    ---
    
    Some information about the dataframe:
    - The main key is the European Article Number (EAN). This can be found under {df['EAN']}
    - Every column name is a specification of the product except for 'Productnummer' and 'EAN'
    - The column names are in Dutch
    - The values in cells might include the unit of the measurement; i.e. Gewicht product might have 8 kg as value and kg here refers to kilogram
    
    The goal of this project:
    - I need you to check if the specifications information I provide is correct
    - Please provide your response in markdown format
    


"""
    return prompt

# - Please also print a dataframe with the following structure: column names: 'Specification', 'Provided_Specs', 'Actual_Specs', 'is_correct'
#     - The values of the dataframe should be the specification name under 'Specification', the value from the dataframe I provide for 'Provided_Specs', the value that you found to be correct under 'Actual_Specs' and the final verdict if the information is correct or incorrect as booelean under 'is_correct' (True of Correct)
#

def generate_prompt_2(df):
    prompt = f"""
    I will ask you to check the specifications of a product for me. can you help with it?
    The product EAN is {df['EAN']}
    The specifications can be found in {df.columns}
    The information is in Dutch language but you can search in any website.
    
    Please share with me your findings in markdown format.
    Please add for every specification, the value you found and whether the information I provided matches the correct one that you found.
    Please check all the specifications I provide at {df}
    Can you provide your answer on which aspects are incorrect and an overall correct percentage? 
    For instance if I gave 20 specifications and 16 of them are correct can you say:
    - From the information you gave 80% is correct!

"""
    return prompt