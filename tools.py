import pandas as pd
from langchain.tools import tool
from langchain_community.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os
from typing import Tuple, List, Dict, Any
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

df = pd.read_csv("filtered_leads.csv", encoding='utf-8')

@tool
def get_lead_info(lead_number: int) -> Dict[str, str]:
    """
    Retrieves information about a lead based on the lead number.

    Args:
        lead_number (str): The lead number to look up.

    Returns:
        Dict[str, str]: A dictionary containing key information about the lead.
    """
    lead = df[df['Lead Number'] == lead_number].iloc[0]
    return {
        "Lead Number": lead['Lead Number'],
        "Company": lead['Company'],
        "Lead Origin": lead['Lead Origin'],
        "Lead Source": lead['Lead Source'],
        "Lead Stage": lead['Lead Stage'],
        "Lead Score": str(lead['Lead Score']),
        "Last Activity": lead['Last Activity'],
        "Last Activity Date": lead['Last Activity Date'],
        "Industry": lead['Industry'],
        "Country": lead['Country']
    }

@tool
def get_lead_activity_summary(lead_number: int) -> Dict[str, any]:
    """
    Retrieves a summary of lead activity based on the lead number.

    Args:
        lead_number (str): The lead number to get the activity summary for.

    Returns:
        Dict[str, any]: A dictionary containing a summary of the lead's activity.
    """
    lead = df[df['Lead Number'] == lead_number].iloc[0]
    
    return {
        "Lead Number": lead_number,
        "Total Visits": int(lead['TotalVisits']) if not pd.isna(lead['TotalVisits']) else 0,
        "Page Views Per Visit": float(lead['Page Views Per Visit']) if not pd.isna(lead['Page Views Per Visit']) else 0,
        "Average Time Per Visit": float(lead['Average Time Per Visit']) if not pd.isna(lead['Average Time Per Visit']) else 0,
        "Last Activity": lead['Last Activity'],
        "Last Activity Date": lead['Last Activity Date']
    }

@tool
def get_lead_source_distribution() -> Dict[str, int]:
    """
    Retrieves the distribution of leads across different lead sources.

    Returns:
        Dict[str, int]: A dictionary with lead sources as keys and the count of leads as values.
    """
    return df['Lead Source'].value_counts().to_dict()

@tool
def get_industry_wise_lead_count() -> Dict[str, int]:
    """
    Retrieves the count of leads for each industry.

    Returns:
        Dict[str, int]: A dictionary with industries as keys and the count of leads as values.
    """
    return df['Industry'].value_counts().to_dict()

@tool
def data_query(query: str, limit: int = 10) -> List[Dict[str, Any]]:
    """
    A universal data query tool that executes a pandas expression on the given DataFrame.

    Args:
        query (str): A valid pandas expression to filter the DataFrame. Example: "df['Lead Source'] == 'Direct Traffic'", "(df['Lead Score'] > 60) & (df['TotalVisits'] <= 5)".
        limit (int): The maximum number of rows to return. Default is 10.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries, each representing a row that matches the query.

    Example usage:
    universal_pandas_query("df['Lead Source'] == 'Direct Traffic'")
    universal_pandas_query("(df['Lead Score'] > 60) & (df['TotalVisits'] <= 5)")
    """
    try:
        # Execute the query
        filtered_df = df[eval(query)]

        # Apply limit
        filtered_df = filtered_df.head(limit) if limit > 0 else filtered_df

        # Convert to list of dictionaries
        results = filtered_df.to_dict('records')

        return results

    except Exception as e:
        return [{"error": f"An error occurred while executing the query: {str(e)}"}]
    
@tool
def generate_personalized_email(
    first_name: str,
    last_name: str,
    product: str,
    product_description: str,
    to_email_address: str
) -> Dict[str, Any]:
    """
    Generates a personalized sales email for a lead.

    Args:
        first_name (str): The first name of the lead.
        last_name (str): The last name of the lead.
        product (str): The name of the product being sold.
        product_description (str): A brief description of the product.
        to_email_address (str): The email address of the lead.

    Returns:
        Dict[str, Any]: A dictionary containing the generated email and metadata.

    Example usage:
    generate_personalized_email("John", "Doe", "AI Assistant", "An advanced AI tool for productivity", "john.doe@example.com")
    """
    try:
        # Initialize the LLM
        llm = OpenAI(temperature=0.7)

        # Create a prompt template
        prompt_template = PromptTemplate(
            input_variables=["first_name", "last_name", "product", "product_description"],
            template="""
            Write a personalized, highly creative sales email to {first_name} {last_name} about the product {product}.
            Product description: {product_description}
            
            The email should be friendly, engaging, and highlight the benefits of the product.
            Do not exceed 200 words. Do not include the subject line or email signature.
            """
        )

        # Create an LLMChain
        chain = LLMChain(llm=llm, prompt=prompt_template)

        # Generate the email content
        email_content = chain.run({
            "first_name": first_name,
            "last_name": last_name,
            "product": product,
            "product_description": product_description
        })

        # Create the result dictionary
        result = {
            "to_email": to_email_address,
            "subject": f"Introducing {product} - Perfect for You, {first_name}!",
            "body": email_content.strip(),
            "metadata": {
                "lead_name": f"{first_name} {last_name}",
                "product": product
            }
        }

        return result

    except Exception as e:
        return {"error": f"An error occurred while generating the email: {str(e)}"}
    
@tool
def send_email(to_email: str, subject: str, body: str) -> bool:
    """
    Sends an email to the specified recipient.

    Args:
        to_email (str): The email address of the recipient.
        subject (str): The subject of the email.
        body (str): The body content of the email.

    Returns:
        bool: True if the email was sent successfully, False otherwise.
    """
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = os.environ['EMAIl_USERNAME']
    msg['To'] = "iamrk98@gmail.com"

    msgText = MIMEText(body, 'plain')
    msg.attach(msgText)

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.login(os.environ['EMAIl_USERNAME'], os.environ['EMAIl_PASSWORD'])
            smtp.sendmail(os.environ['EMAIl_USERNAME'], to_email, msg.as_string())
            print(f"Email sent to {to_email}")

    except Exception as e:
            print(e)