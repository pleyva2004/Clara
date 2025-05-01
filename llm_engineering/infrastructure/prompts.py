def email_classifier_prompt(sender: str, subject: str, body_snippet: str) -> str:
    prompt = f"""
    Classify the following email and return a JSON object with the following structure:
    {{
        "category": "Alumni" | "Company" | "Internal NJIT Partner" | "Unrelated",
        "meta_data": "string"
    }}

    Rules for meta_data:
    - If category is "Company": meta_data should be the company name
    - If category is "Alumni": meta_data should be the alumni name
    - If category is "Internal NJIT Partner": meta_data should be the partner name
    - If category is "Unrelated": meta_data should be "Unrelated"

    Email from: {sender}
    Subject: {subject}
    Body snippet: {body_snippet}

    Return ONLY the JSON object and nothing else.
    """
    return prompt


def readEmailPrompt(email: str) -> str:
    prompt = f"""


    Read the following email:
    {email}

    Return the email in a structured format with the following fields:
    **Introduction of Sender**:
        *   Name: 
        *   Title: 
        *   Company/Affiliation/Organization: 


    **Purpose of Email**:


    **Call to Action**:
    """
    return prompt


def createMessagePrompt(email_summary: str) -> str:
    prompt = f"""
    Create a one paragraph message for Whatsapp group on the following information:
    {email_summary}

    Always start with "Hola Familia!". Make the message concise and to the point. Always include the Call to Action points bys saying "They are asking for..." folowed by a bulleted list of the Call to Action points.
    Finally, finish off by saying "How would you like me to respond?"

    """
    return prompt


def validateMessagePrompt(message: str, email_summary: str, email: list) -> str:
    prompt = f"""
    MESSAGE TO VALIDATE:
    {message}

    SOURCE INFORMATION:
    1. Email Summary:
    {email_summary}

    2. Original Email:
    {email}

    Validation Requirements:

    1. Accuracy Score (0-100):
       - Score 100: Perfect accuracy and completeness
       - Score 70-99: Minor discrepancies or omissions
       - Score 40-69: Significant discrepancies or missing information
       - Score 0-39: Major inaccuracies or missing critical content

    2. Format Compliance Check:
       - Must start with "Hola Familia!"
       - Must list action items after "They are asking for:" with bullet points
       - Must end with "How would you like me to respond?"

    3. Discrepancy Analysis:
       - List any factual errors between message and source materials
       - Each discrepancy should be specific and actionable
       - Include exact details of what is incorrect

    4. Missing Information Check:
       - Identify any important details from source materials not included in message
       - Focus on essential information only

    5. Correction Guidelines:
       - Provide specific, actionable corrections for each issue
       - Include both content and format corrections
       - List corrections in order of importance

    IMPORTANT: Respond ONLY with a JSON object in the following format:
    
        "accuracy_score": <number between 0-100>,
        "format_compliant": <boolean>,
        "factual_discrepancies": [<list of strings describing any factual errors>],
        "missing_information": [<list of strings describing important missing details>],
        "suggested_corrections": [<list of strings with specific corrections>]
    

    The accuracy_score and format_compliant fields are required. Other fields should be included if relevant issues are found.
    """
    return prompt

