# import modules
import os
import pandas as pd
import openai
# from openai import InvalidRequestError
import time
import json
from json import JSONDecodeError
from tqdm import tqdm
import textwrap
# from google.api_core import retry
# from google.generativeai.types import RequestOptions

# import google.generativeai as genai
# from google import genai
import google.generativeai as genai
from openai import OpenAI
# Initialize the Llama API client
# client = OpenAI(base_url="http://10.185.151.234:1234/v1", api_key="lm-studio")
# add a progress bar to pandas operations
tqdm.pandas(desc='CVs')

# define the path to the output CSV file
output_csv_file_path = '../Output/CVs_Info_Extracted.csv'

# define the path to the output Excel file
output_excel_file_path = '../Output/CVs_Info_Extracted.xlsx'


# define a class to extract CV information
class CVsInfoExtractor:
    # define a constructor that initializes the class with a DataFrame of CVs
    def __init__(self, cvs_df, openai_api_key):
        # Initialize Gemini API (Ensure API key is set up before calling this)
        genai.configure(api_key=openai_api_key)  # Replace with your actual API key
        # self.client = genai.Client(api_key = openai_api_key)
        self.cvs_df = cvs_df
        
        # open a file in read mode and read the contents of the file into a variable
        with open('../Engineered_Prompt/alma_prompt.txt', 'r') as file:
            self.prompt = file.read()
        
        # open a file in read mode and read the contents of the file into a variable
        with open('../Engineered_Prompt/Extraction_prompt.txt', 'r') as file:
            self.extraction_prompt = file.read()
        
        # open a file in read mode and read the contents of the file into a variable
        with open('../Engineered_Prompt/o1a_classification_prompt.txt', 'r') as file:
            self.classification_prompt = file.read()
        
        # Join the desired positions into a comma-separated string
        # suitable_positions_str = "(" + ", ".join(desired_positions) + ")"

        # Replace the placeholder in the prompt with the formatted suitable positions string
        # self.prompt = self.prompt.replace('(suitable position for the candidate)', suitable_positions_str)
        
        
        # set the OpenAI API key
        openai.api_key = openai_api_key


    # define internal function to call GPT for CV info extraction
    # Define internal function to call GPT for CV info extraction
    def _call_gpt_for_cv_info_extraction(self, prompt, cv_content, model, temperature=0):
        # print(cv_content)
        # Create a dict of parameters for the ChatCompletion API
        completion_params = {
            'model': model,
            'messages': [
                {"role": "system", "content": prompt},
                {"role": "user", "content": cv_content}
            ],
            'temperature': temperature
        }

        # Send a request to the ChatCompletion API and store the response
        response = client.chat.completions.create(**completion_params)

        # If the response contains choices and at least one choice, extract the message content
        if response.choices and len(response.choices) > 0:
            cleaned_response = response.choices[0].message.content
            print(cleaned_response)
            try:
                # Try to convert the message content to a JSON object
                json_response = json.loads(cleaned_response)
            except json.JSONDecodeError:
                # If the conversion fails, set the JSON response to None
                json_response = None  
        else:
            # If the response does not contain choices or no choice, set the JSON response to None
            json_response = None

        # Return the JSON response
        return json_response
    


    def _call_gemini_for_cv_info_extraction(self, prompt, cv_content, model="gemini-2.0-pro-exp", temperature=0):
        try:
            model = genai.GenerativeModel('models/' + model)
            # Create a request to the Gemini model
            response = model.generate_content(
                contents=[
                    {"role": "user", "parts": [{"text": prompt}]},
                    {"role": "user", "parts": [{"text": cv_content}]}
                ],
                generation_config={"temperature": temperature})
        #     request_options=RequestOptions(
        # retry=retry.Retry(initial=1, multiplier=1, maximum=60))
            # Extract response text
            cleaned_response = response.text if response.text else ""
            print(cleaned_response)  # Debugging

            return cleaned_response  # Gemini doesn't return JSON by default, so returning plain text

        except Exception as e:
            print(f"Error in Gemini API call: {str(e)}")
            return None


    
    # Defines internal function to normalize a JSON response from GPT
    def _normalize_gpt_json_response(self, CV_Filename, json_response):
        
        # Creates a DataFrame with one column "CV_Filename", the values of this column is from the "CV_Filename"
        CV_Filename_df = pd.DataFrame([CV_Filename], columns = ['CV_Filename'])

        # Creates a DataFrame with one column "All_Info_JSON", the values of this column is the JSON response
        df_CV_Info_Json = pd.DataFrame([[json_response]], columns = ['All_Info_JSON'])

        # Normalize the JSON response, flattening it into a table
        df_CV_Info_Json_normalized = pd.json_normalize(json_response)

        # Concatenates the three DataFrame along the columns
        df = pd.concat([CV_Filename_df, df_CV_Info_Json_normalized, df_CV_Info_Json], axis=1)
        
        # Returns the final DataFrame
        return df


    # Defines internal function to write the DataFrame into a CSV file
    def _write_response_to_file(self, df):

        # Checks if the output CSV file already exists
        if os.path.isfile(output_csv_file_path):
            # If the file exists, append the DataFrame into the CSV file without writing headers
            df.to_csv(output_csv_file_path, mode='a', index=False, header=False)
        else:
            # If the file doesn't exist, write the DataFrame into a new CSV file
            df.to_csv(output_csv_file_path, mode='w', index=False)

    def _gemini_pipeline(self, row):
        # Retrieve the CV Filename and Content
        CV_Filename = row['CV_Filename']
        CV_Content = row['CV_Content']

        print(f"Processing CV in chunks for {CV_Filename}...")

        # Break CV content into smaller parts
        chunk_size = 3000  # Adjust based on token limits
        chunks = textwrap.wrap(CV_Content, width=chunk_size, break_long_words=False, break_on_hyphens=False)

        extracted_info = ""  # Store cumulative extracted information

        for i, chunk in enumerate(chunks):
            print(f"Processing chunk {i+1}/{len(chunks)} for {CV_Filename}...")

            # Sleep to avoid API rate limits
            time.sleep(30)

            # Call GPT for extracting structured information from each chunk
            response = self._call_gemini_for_cv_info_extraction(
                prompt=self.extraction_prompt,
                cv_content=chunk,
            )

            print(f"Chunk {i+1} Response:\n{response}\n")  # Debugging: Print response

            # Accumulate extracted information
            extracted_info += response + "\n"

        # Save extracted information to a text file
        output_directory = "extracted_info"
        os.makedirs(output_directory, exist_ok=True)
        extracted_info_path = os.path.join(output_directory, f"{CV_Filename}_extracted.txt")

        with open(extracted_info_path, "w", encoding="utf-8") as file:
            file.write(extracted_info)

        print(f"Extracted information saved to: {extracted_info_path}")

        # Sleep to avoid API rate limits
        time.sleep(60)
        # Pass extracted information through O-1A assessment
        print(f"Assessing O-1A qualifications for {CV_Filename}...")

        o1a_response = self._call_gemini_for_cv_info_extraction(
            prompt=self.prompt,  # This is the refined O-1A prompt
            cv_content=extracted_info,
        )

        # Save O-1A assessment results to a text file
        CV_Filename_without_extn = os.path.splitext(row['CV_Filename'])[0]  # Remove .pdf extension
        o1a_info_path = os.path.join(output_directory, f"{CV_Filename_without_extn}_O1A_assessment.txt")

        with open(o1a_info_path, "w", encoding="utf-8") as file:
            file.write(o1a_response)

        print(f"O-1A assessment saved to: {o1a_info_path}")

        # return o1a_response  # Return the final O-1A assessment    # Define the internal function _write_final_results_to_excel
        # Sleep before final classification call
        time.sleep(30)

        # Final classification for low/medium/high
        print(f"Classifying O-1A eligibility for {CV_Filename}...")

        final_classification = self._call_gemini_for_cv_info_extraction(
            prompt=self.classification_prompt,  # Uses the final classification prompt
            cv_content=o1a_response,
        )

        # Save final classification result
        classification_info_path = os.path.join(output_directory, f"{CV_Filename_without_extn}_O1A_classification.txt")

        with open(classification_info_path, "w", encoding="utf-8") as file:
            file.write(final_classification.strip())  # Ensure it's a one-word response

        print(f"Final classification saved to: {classification_info_path}")

        # return o1a_response, final_classification.strip()  # Return the final classification result
        return {
            "CV_Filename": CV_Filename,
            "Extracted_Info": json.dumps(extracted_info.strip(), indent=2, ensure_ascii=False),
            "O1A_Response": json.dumps(o1a_response.strip(), indent=2, ensure_ascii=False),
            "Final_Classification": final_classification.strip()
        }
    def _write_final_results_to_excel(self):
        # Load the CSV file into a pandas DataFrame
        df_to_excel = pd.read_csv(output_csv_file_path)

        # Write the DataFrame to an Excel file
        df_to_excel.to_excel(output_excel_file_path)

        # Return the DataFrame
        return df_to_excel

    def extract_cv_info(self):
        print('---- Executing ResumeGPT Pipeline ----')
        print('----------------------------------------------')

        results = self.cvs_df.progress_apply(self._gemini_pipeline, axis=1)

        print('Extraction Completed!')

        return results.to_list()  # Return results as a list of dictionaries

