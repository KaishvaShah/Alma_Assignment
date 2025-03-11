# Alma_Assignment
# **📌 Process Overview**  

This project automates **CV processing** to assess a candidate’s **O-1A visa eligibility** using **FastAPI, OCR, and LLMs (Gemini API)**. It extracts relevant information, evaluates qualifications, and provides a structured **JSON output**.  

## **🔧 What You Will Need**  

Before you begin, make sure you have the following:

1. **Gemini API Key**  
   - You will need a **Gemini API key** for processing. Don’t worry, the model I am using provides free usage for a certain frequency of calls, and I have already optimized the pipeline to stay within those limits.

2. **FASTAPI Installation**  
   - You need to have **FastAPI** installed on your system to run the application. If you don’t have it yet, you can install it easily using the following command:  
   ```bash
   pip install fastapi
   ```

---

## **⚠️ Disclaimer**

This project is built on top of an existing codebase from [ResumeGPT by Aillian](https://github.com/Aillian/ResumeGPT.git). Here are the key points of customization:

- I modified the original GPT-4 calls in the code and replaced them with **Gemini API calls** for enhanced processing.  
- After extracting the information from resumes, I created a new pipeline to assess the candidate's eligibility for an O-1A visa, providing a more tailored and specific output.

## **🔹 Step-by-Step Procedure**  

### **1️⃣ Upload & Input Handling**  
📥 **What Happens?**  
- The user uploads **one or more CVs** via a **FastAPI endpoint**.  
- The system accepts files in **PDF or text format**.  

📌 **Key Components:**  
- `FastAPI` handles **file uploads** via an API endpoint.  
- `CVsReader` processes the uploaded files.  

📂 **Example Input:**  
```
POST /upload
Files: ["John_Doe_CV.pdf", "Jane_Smith_CV.pdf"]
```

---

### **2️⃣ OCR & Text Extraction**  
🔍 **What Happens?**  
- If the file is a **PDF**, it is processed using **OCR (Optical Character Recognition)**.  
- Extracts **raw text** from the document.  

📌 **Key Components:**  
- `PyMuPDF` (for direct text extraction from PDFs).  
- `pytesseract` (for OCR when text extraction fails).  

📝 **Example Output:**  
```
"John Doe is a researcher at MIT... He has published papers in IEEE..."
```

---

### **3️⃣ Chunking & Preprocessing**  
📦 **What Happens?**  
- The extracted CV text is **split into smaller chunks** (to fit within LLM token limits).  
- Each chunk is **sent separately** to the **Gemini API (because I needed a free LLM api)** for processing.  

📌 **Key Components:**  
- `textwrap.wrap()` (splits text into **3000-character chunks**).  
- **Sleep timers** are used to avoid rate limits. That is why you see a quite slow inference (it is deliberate). I am spending time instead of money.  

---

### **4️⃣ Information Extraction using LLM**  
🤖 **What Happens?**  
- Each text chunk is sent to the **Gemini API** using a **predefined prompt**.  
- The model extracts **achievements** that match **O-1A visa criteria**.  

📌 **Key Components:**  
- `_call_gemini_for_cv_info_extraction()` sends prompts to Gemini.  Look at the following file \ResumeGPT\Engineered_Prompt\Extraction_prompt.txt.
- **8 O-1A criteria** (awards, publications, judging, contributions, memberships, leadership, salary, media).  

📜 **Example Output:**  
```json
{
  "Published_Research": "IEEE Signal Processing, 2025",
  "Awards": "KVPY Scholarship (2020)"
}
```

---

### **5️⃣ O-1A Evaluation**  
📊 **What Happens?**  
- The extracted info is **re-analyzed** by the **Gemini API** using a refined **O-1A evaluation prompt** (see ResumeGPT\Engineered_Prompt\alma_prompt.txt).  
- It determines **how many criteria the candidate meets**.  

📌 **Key Components:**  
- `_call_gemini_for_cv_info_extraction()` runs the **O-1A assessment prompt**.  
- Outputs **detailed reasoning** on how many **criteria** are satisfied.  

📝 **Example Output:**  
- Secured All India Rank 1373 in JEE Advanced among 150,000 students [’20]
- Awarded a Change of Branch to Electrical Engineering among 24 students due to outstanding academics [’22]
- Stood 2nd place school-wide in the badminton competition at Sri Chaitanya School [’16]
- Published Research Papers & Articles: Reconstruction from Samples at Unknown Locations with Application to 2D Unknown View Tomography - Elsevier Signal Processing
- Developed gradient descent based tomographic reconstruction algorithms using von Mises distributions and a PMF model for improved 2D accuracy.
- Implemented Wiener filter-based PCA and eigenvector decomposition for denoising.

```

---

### **6️⃣ Final Classification (Low/Medium/High)**  
🏅 **What Happens?**  
- A **final LLM call** classifies eligibility as `"low"`, `"medium"`, or `"high"`. I understand from the documentation that we need just 3 criteria satisfied, but since there is a heavy use of LLMs this classification needs to be a little more harsh.  
- Rules:  
  - **3 or fewer criteria** → `"low"`  
  - **4 or 5 criteria** → `"medium"`  
  - **6+ criteria** → `"high"`  

📌 **Key Components:**  
- **LLM prompt** strictly returns `"low"`, `"medium"`, or `"high"`.  
- `_call_gemini_for_cv_info_extraction()` sends classification prompt.  

🏆 **Example Output:**  
```json
{
  "Final_Classification": "medium"
}
```

---

### **7️⃣ FastAPI JSON Output**  
📤 **What Happens?**  
- The final structured output is returned via FastAPI in **JSON format**.  
- JSON is **clean & formatted** for integration into other systems.  

📌 **Key Components:**  
- `return` statement in FastAPI delivers **structured JSON**.  

📜 **Final JSON Output:**  
```json
{
  "CV_Filename": "John_Doe_CV.pdf",
  "Extracted_Info": "Published 2 research papers in IEEE. Won KVPY scholarship.",
  "O1A_Response": "Candidate meets 3 criteria: Published Research, Awards, Judging.",
  "Final_Classification": "medium"
}
```

---

## **🎯 Summary of Key Technologies Used**  
| **Component**            | **Technology Used** |
|-------------------------|-------------------|
| File Upload            | FastAPI           |
| OCR & Text Extraction  | PyMuPDF, pytesseract |
| Chunking & Processing  | textwrap, sleep timers |
| LLM Information Extraction | Gemini API (via OpenAI-like call) |
| O-1A Criteria Evaluation | Gemini API       |
| Final Classification   | LLM (Prompt-based) |
| API Output             | FastAPI (JSON response) |

---

Does this **expanded breakdown** work for your README? 🚀 Let me know if you'd like **additional sections** (e.g., **installation, setup, running commands**).

