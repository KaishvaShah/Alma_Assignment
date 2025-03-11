# import modules
import os
from PyPDF2 import PdfReader
import pandas as pd
from tqdm import tqdm
import re

# Define a class to read CVs from a directory
class CVsReader:
    
    # Initialize the class with the directory path where CVs are located
    def __init__(self, cvs_directory_path):
        self.cvs_directory_path = cvs_directory_path


    # Method to read new CV files from the given directory
    def _read_new_directory_files(self):

        # Store the directory path of CVs
        cvs_directory_path = self.cvs_directory_path

        # Store the path of the CSV file where previously extracted CVs are stored
        previously_extracted_cvs_path = '../Output/CVs_Info_Extracted.csv'

        # Get a list of all files in the CVs directory
        all_cvs = os.listdir(cvs_directory_path)

        # If there is a CSV file of previously extracted CVs
        # if os.path.isfile(previously_extracted_cvs_path):

        #     # Read that file and get the filenames of CVs
        #     previously_extracted_cvs = pd.read_csv(previously_extracted_cvs_path, usecols = ['CV_Filename'])

        #     # Convert those filenames to a list
        #     previously_extracted_cvs = previously_extracted_cvs.CV_Filename.to_list()

        #     # Filter out the CVs that have already been processed
        #     all_cvs = [cv for cv in all_cvs if cv not in previously_extracted_cvs]

        # Print the number of CVs that are left to be processed
        print(f'Number of CVs to be processed: {len(all_cvs)}')

        # Return the list of CVs to be processed
        return all_cvs


    # Method to extract text from a PDF file
    def _extract_text_from_pdf(self, pdf_path):

        # Print the name of the file being processed
        print(f"Extracting text from file: {pdf_path}")

        # Create a PdfReader object
        pdf = PdfReader(pdf_path)

        # Initialize an empty string to store the extracted text
        text = ''

        # Loop over the pages in the pdf
        for page in range(len(pdf.pages)):

            # Extract text from each page and append it to the text string
            text += pdf.pages[page].extract_text()

        # Return the extracted text
        return text

    
    # Define a method that reads PDF content from a directory
    def _read_pdfs_content_from_directory(self, directory_path):
        
        # Initialize a dictionary to hold the filenames and contents of the CVs
        data = {'CV_Filename': [], 'CV_Content': []}
        
        # Read all the new files in the directory
        all_cvs = self._read_new_directory_files()
        
        # For each file in the directory
        for filename in tqdm(all_cvs, desc='CVs'):
            # If the file is a PDF
            if filename.endswith('.pdf'):
                # Construct the full file path
                file_path = os.path.join(directory_path, filename)
                try:
                    # Extract the text content from the PDF
                    content = self._extract_text_from_pdf(file_path)
                    # Add the filename to the dictionary
                    data['CV_Filename'].append(filename)
                    # Add the content to the dictionary
                    data['CV_Content'].append(content)
                except Exception as e:
                    # Print the exception if there is an error in reading the file
                    print(f"Error reading file {filename}: {e}")
        # Return the data as a DataFrame
        return pd.DataFrame(data)


    # # Define a method that reads and cleans CVs
    # def read_cv(self):
        
    #     # Print a message indicating the start of the CV extraction process
    #     print('---- Excecuting CVs Content Extraction Process ----')
        
    #     # Read the PDFs from the directory and store their content in a DataFrame
    #     df = self._read_pdfs_content_from_directory(self.cvs_directory_path)
        
    #     # Print a message indicating the start of the CV content cleaning process
    #     print('Cleaning CVs Content...')
    #     # Clean the CV content by replacing newline characters and trailing spaces with a single newline character
    #     df['CV_Content'] = df['CV_Content'].str.replace(r"\n(?:\s*)", "\n", regex=True)
    #     # Print a message indicating the end of the CV extraction process
    #     print('CVs Content Extraction Process Completed!')
    #     print('----------------------------------------------')
    #     # Return the DataFrame
    #     return df
    # def read_cv(self):
    #     # Print a message indicating the start of the CV extraction process
    #     print('---- Executing CVs Content Extraction Process ----')

    #     # Read the PDFs from the directory and store their content in a DataFrame
    #     df = self._read_pdfs_content_from_directory(self.cvs_directory_path)

    #     # Print a message indicating the start of the CV content cleaning process
    #     print('Cleaning CVs Content...')

    #     # Define unwanted sections (Skills, Courses, etc.)
    #     unwanted_sections = [
    #         r"(?i)\bSkills\b.*?(?=\n[A-Z]|\Z)",   # Match "Skills" section until the next capitalized header
    #         r"(?i)\bCertifications\b.*?(?=\n[A-Z]|\Z)",  # Match "Certifications" section
    #         r"(?i)\bCourses\b.*?(?=\n[A-Z]|\Z)",  # Match "Courses" section
    #         r"(?i)\bTechnical Skills\b.*?(?=\n[A-Z]|\Z)",  # Match "Technical Skills" section
    #         r"(?i)\bSoft Skills\b.*?(?=\n[A-Z]|\Z)",  # Match "Soft Skills" section
    #     ]

    #     # Remove unwanted sections from CV content
    #     for pattern in unwanted_sections:
    #         df['CV_Content'] = df['CV_Content'].str.replace(pattern, '', flags=re.DOTALL)

    #     # Clean extra newlines and spaces
    #     df['CV_Content'] = df['CV_Content'].str.replace(r"\n(?:\s*)", "\n", regex=True)

    #     # Print a message indicating the end of the CV extraction process
    #     print('CVs Content Extraction Process Completed!')
    #     print('----------------------------------------------')

    #     # Return the cleaned DataFrame
    #     return df

    # def read_cv(self):
    #     print('---- Executing CVs Content Extraction Process ----')
        
    #     # Read the PDFs and store content in a DataFrame
    #     df = self._read_pdfs_content_from_directory(self.cvs_directory_path)

    #     print('Extracting CV Sections...')

    #     # Define sections to extract
    #     sections = {
    #         "Education": r"(?i)\bEducation\b[\s\S]*?(?=\n[A-Z]|\Z)",
    #         "Experience": r"(?i)\bExperience\b[\s\S]*?(?=\n[A-Z]|\Z)",
    #         "Projects": r"(?i)\b(Projects|Research)\b[\s\S]*?(?=\n[A-Z]|\Z)",
    #         "Skills": r"(?i)\bSkills\b[\s\S]*?(?=\n[A-Z]|\Z)",
    #         "Certifications": r"(?i)\b(Certifications|Courses)\b[\s\S]*?(?=\n[A-Z]|\Z)",
    #         "Awards": r"(?i)\b(Awards|Achievements|Honors)\b[\s\S]*?(?=\n[A-Z]|\Z)",
    #         "Publications": r"(?i)\b(Publications|Research Papers)\b[\s\S]*?(?=\n[A-Z]|\Z)",
    #     }
    #     print(df["CV_Content"])
    #     # Extract sections and store in the DataFrame
    #     for section, pattern in sections.items():
    #         df[section] = df['CV_Content'].apply(lambda x: re.search(pattern, x, re.DOTALL).group(0) if re.search(pattern, x, re.DOTALL) else "")
    #     print(df.describe())
    #     # Remove extra spaces and newlines
    #     for col in sections.keys():
    #         df[col] = df[col].str.strip().replace(r"\n\s*", "\n", regex=True)

    #     # Drop the full CV content if no longer needed
    #     # df.drop(columns=["CV_Content"], inplace=True)

    #     print('CV Sections Extracted Successfully!')
    #     print('----------------------------------------------')

    #     return df
    # def read_cv(self):
    #     print('---- Executing CVs Content Extraction Process ----')
        
    #     # Read the PDFs and store content in a DataFrame
    #     df = self._read_pdfs_content_from_directory(self.cvs_directory_path)
    #     print(df['CV_Content'])
    #     print('Extracting CV Sections...')

    #     # Define sections to extract with more comprehensive patterns
    #     sections = {
    #         "Education": r"(?i)(?:^|\n)(?:\s*)(Education|Academic Background|Educational Qualifications)(?:\s*):?(?:\s*)[\s\S]*?(?=\n\s*(?:[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s*:?|\Z))",
    #         "Experience": r"(?i)(?:^|\n)(?:\s*)(Experience|Work Experience|Professional Experience|Employment History)(?:\s*):?(?:\s*)[\s\S]*?(?=\n\s*(?:[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s*:?|\Z))",
    #         "Projects": r"(?i)(?:^|\n)(?:\s*)(Projects|Project Work|Research Projects|Research Work)(?:\s*):?(?:\s*)[\s\S]*?(?=\n\s*(?:[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s*:?|\Z))",
    #         "Skills": r"(?i)(?:^|\n)(?:\s*)(Skills|Technical Skills|Core Competencies|Key Skills|Expertise)(?:\s*):?(?:\s*)[\s\S]*?(?=\n\s*(?:[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s*:?|\Z))",
    #         "Certifications": r"(?i)(?:^|\n)(?:\s*)(Certifications|Courses|Professional Certifications|Training)(?:\s*):?(?:\s*)[\s\S]*?(?=\n\s*(?:[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s*:?|\Z))",
    #         "Awards": r"(?i)(?:^|\n)(?:\s*)(Awards|Achievements|Honors|Recognitions)(?:\s*):?(?:\s*)[\s\S]*?(?=\n\s*(?:[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s*:?|\Z))",
    #         "Publications": r"(?i)(?:^|\n)(?:\s*)(Publications|Research Papers|Papers|Articles)(?:\s*):?(?:\s*)[\s\S]*?(?=\n\s*(?:[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s*:?|\Z))",
    #     }

    #     try:
    #         # Check and convert CV_Content to string if needed
    #         if 'CV_Content' in df.columns:
    #             # Convert any non-string values to strings
    #             df['CV_Content'] = df['CV_Content'].fillna("").astype(str)
                
    #             # Print a sample to verify content
    #             print(f"Sample CV content (first 200 chars): {df['CV_Content'].iloc[0][:200] if len(df) > 0 else 'No content'}")
    #         else:
    #             print("Warning: 'CV_Content' column not found in DataFrame")
    #             return df
            
    #         # Extract sections and store in the DataFrame
    #         for section, pattern in sections.items():
    #             df[section] = df['CV_Content'].apply(
    #                 lambda x: re.search(pattern, x, re.DOTALL).group(0) if re.search(pattern, x, re.DOTALL) else ""
    #             )
    #             print("For the section", section, df[section])
    #         # print(df.columns())
    #         # # print(df['Education'])
    #         # Clean extracted sections - convert to string first to avoid str accessor issues
    #         for col in sections.keys():
    #             if col in df.columns:
    #                 # Fill NA values and ensure string type before using str methods
    #                 df[col] = df[col].fillna("").astype(str)
    #                 df[col] = df[col].str.strip().replace(r"\n\s*", "\n", regex=True)
            
    #         # Calculate simple statistics
    #         print("\nExtraction Results:")
    #         for section in sections.keys():
    #             if section in df.columns:
    #                 found_count = (df[section].str.len() > 10).sum()
    #                 print(f"  - {section}: Found in {found_count} out of {len(df)} CVs")
                
    #         print('\nCV Sections Extracted Successfully!')
    #         print('----------------------------------------------')
            
    #     except Exception as e:
    #         print(f"Error during section extraction: {str(e)}")
    #         # Print more diagnostic information
    #         print(f"DataFrame info:")
    #         print(df.info())
    #         print("\nDataFrame columns:", df.columns.tolist())
            
    #     return df

    def read_cv(self):
        print('---- Executing CVs Content Extraction Process ----')

        # Read the PDFs and store content in a DataFrame
        df = self._read_pdfs_content_from_directory(self.cvs_directory_path)

        print('Extracting CV Sections...')

        # Define improved regex patterns for section extraction
        sections = {
            "Education": r"(?i)(?:^|\n)(Education|Academic Background|Educational Qualifications|Academic Qualification)[\s\n]*([\s\S]*?)(?=\n[A-Z][a-z]|$)",
            "Experience": r"(?i)(?:^|\n)(Work Experience|Experience|Professional Experience|Employment History|Internships)[\s\n]*([\s\S]*?)(?=\n[A-Z][a-z]|$)",
            "Projects": r"(?i)(?:^|\n)(Projects|Project Work|Research Projects|Research Work|Academic Projects|Technical Projects)[\s\n]*([\s\S]*?)(?=\n[A-Z][a-z]|$)",
            "Skills": r"(?i)(?:^|\n)(Skills|Technical Skills|Core Competencies|Key Skills|Expertise)[\s\n]*([\s\S]*?)(?=\n[A-Z][a-z]|$)",
            "Certifications": r"(?i)(?:^|\n)(Certifications|Courses|Professional Certifications|Training)[\s\n]*([\s\S]*?)(?=\n[A-Z][a-z]|$)",
            "Awards": r"(?i)(?:^|\n)(Awards|Achievements|Honors|Recognitions)[\s\n]*([\s\S]*?)(?=\n[A-Z][a-z]|$)",
            "Publications": r"(?i)(?:^|\n)(Publications|Research Papers|Papers|Articles|Academic Projects (Research))[\s\n]*([\s\S]*?)(?=\n[A-Z][a-z]|$)",
        }

        try:
            # Ensure 'CV_Content' is a valid string column
            if 'CV_Content' in df.columns:
                df['CV_Content'] = df['CV_Content'].fillna("").astype(str)
                print(f"Sample CV content (first 200 chars): {df['CV_Content'].iloc[0][:200] if len(df) > 0 else 'No content'}")
            else:
                print("Warning: 'CV_Content' column not found in DataFrame")
                return df

            # Extract sections and store them in the DataFrame
            for section, pattern in sections.items():
                df[section] = df['CV_Content'].apply(
                    lambda x: re.search(pattern, x, re.DOTALL).group(2).strip() if re.search(pattern, x, re.DOTALL) else ""
                )

            # Clean extracted sections (remove unnecessary spaces and newlines)
            for col in sections.keys():
                df[col] = df[col].fillna("").astype(str).str.strip().replace(r"\n\s*", "\n", regex=True)

            # Print extraction summary
            print("\nExtraction Results:")
            for section in sections.keys():
                found_count = (df[section].str.len() > 10).sum()
                print(f"  - {section}: Extracted from {found_count} out of {len(df)} CVs")
            
            print('\nCV Sections Extracted Successfully!')
            print('----------------------------------------------')

        except Exception as e:
            print(f"Error during section extraction: {str(e)}")
            print(f"DataFrame info:")
            print(df.info())
            print("\nDataFrame columns:", df.columns.tolist())
        print("\nSample Extracted Sections:")
        for i in range(min(3, len(df))):  # Print up to 3 CVs
            print(f"\nCV {i+1}: {df['CV_Filename'].iloc[i]}")
            for section in sections.keys():
                print(f"\n--- {section} ---")
                print(df[section].iloc[i][:500])  # Print only first 500 characters to avoid long output
            print("\n" + "="*50)  # Separator for better readability
        return df
