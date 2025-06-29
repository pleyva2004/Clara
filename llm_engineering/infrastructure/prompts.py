def emailClassifierPrompt(sender: str, subject: str, body_snippet: str) -> str:
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


    If the email contains dates, make sure to include the date in the Purpose of Email section.
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


def validateMessagePrompt(message: str, email_summary: str, email: str) -> str:
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

def editMessagePrompt(message: str, edits: str, context: str) -> str:
    prompt = f"""
    MESSAGE TO EDIT:
    {message}

    EDITS TO MAKE:
    {edits}

    CONTEXT:
    {context}

    Edit the message to make the necessary changes. Make sure to keep the original message structure and format. Include all the edits. Return ONLY the new edited message and nothing else.
    """
    return prompt

def validateResponsePrompt(response: str, email_summary: str) -> str:

    prompt = f"""
    RESPONSE TO VALIDATE:
    {response}

    SOURCE INFORMATION:
    1. Email Summary:
    {email_summary}
    
    Validation Requirements:

    1. Accuracy Score (0-100):
       - Score 100: Response addresses ALL action items from the message completely
       - Score 70-99: Response addresses most action items but may be missing minor details
       - Score 40-69: Response addresses some action items but is missing significant ones
       - Score 0-39: Response fails to address most or all action items

    2. Missing Information Check:
       - Extract ALL action items from the email summary (usually listed after "Call to Action:")
       - Check if EACH action item is addressed in the response
       - List any action items that are NOT addressed in the response

    3. Correction Guidelines:
       - Provide specific suggestions for addressing any missing action items
       - Focus on completeness of response to action items

    IMPORTANT: Respond ONLY with a JSON object in the following format:
    
        "accuracy_score": <number between 0-100>,
        "action_items_in_message": [<list of action items extracted from the message>],
        "action_items_addressed": [<list of action items that were addressed in the response>],
        "missing_information": [<list of action items NOT addressed in the response>],
        "suggested_corrections": [<list of specific suggestions to address missing items>]

    The accuracy_score field is required. Other fields should be included to show the analysis.
    """
    return prompt

def requestMissingInformationPrompt(response: str, action_items_in_message: str, action_items_addressed: str, missing_information: str, suggested_corrections: str) -> str:
    prompt = f"""
    RESPONSE GIVEN BY USER:
    {response}

    ACTION ITEMS IN MESSAGE:
    {action_items_in_message}

    ACTION ITEMS ADDRESSED:
    {action_items_addressed}

    MISSING INFORMATION:
    {missing_information}

    SUGGESTED CORRECTIONS:
    {suggested_corrections}


    
    INSTRUCTIONS:

    Your task is to edit the response to address all missing action items. Follow these steps:

    1. Review the original response and identify what was addressed correctly
    2. For each missing action item:
       - Add a polite request for the specific missing information
       - Use the suggested corrections as guidance
    3. Structure the response to:
       - Acknowledge the information already provided
       - Clearly state what additional information is needed
       - Make it easy for the recipient to provide the missing details

    Create a new response that:
    - Acknowledges the helpful parts of the original response
    - Adds clear requests for missing information
    - Follows a logical flow
    - Makes it easy for the recipient to understand what additional information is needed

    Return ONLY the edited response with no additional commentary or meta-text.

    """
    return prompt