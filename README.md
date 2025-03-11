# Alma_Assignment
Here’s an **expanded** breakdown of every step in the **O-1A Eligibility Assessment Pipeline** for the README:  

---

# **📌 Process Overview**  

This project automates **CV processing** to assess a candidate’s **O-1A visa eligibility** using **FastAPI, OCR, and LLMs (Gemini API)**. It extracts relevant information, evaluates qualifications, and provides a structured **JSON output**.  

---

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
- Each chunk is **sent separately** to the **Gemini API** for processing.  

📌 **Key Components:**  
- `textwrap.wrap()` (splits text into **3000-character chunks**).  
- **Sleep timers** are used to avoid rate limits.  

---

### **4️⃣ Information Extraction using LLM**  
🤖 **What Happens?**  
- Each text chunk is sent to the **Gemini API** using a **predefined prompt**.  
- The model extracts **achievements** that match **O-1A visa criteria**.  

📌 **Key Components:**  
- `_call_gemini_for_cv_info_extraction()` sends prompts to Gemini.  
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
- The extracted info is **re-analyzed** by the **Gemini API** using a refined **O-1A evaluation prompt**.  
- It determines **how many criteria the candidate meets**.  

📌 **Key Components:**  
- `_call_gemini_for_cv_info_extraction()` runs the **O-1A assessment prompt**.  
- Outputs **detailed reasoning** on how many **criteria** are satisfied.  

📝 **Example Output:**  
```json
{
  "Met_Criteria": ["Published Research", "Awards", "Judging"],
  "Criteria_Count": 3
}
```

---

### **6️⃣ Final Classification (Low/Medium/High)**  
🏅 **What Happens?**  
- A **final LLM call** classifies eligibility as `"low"`, `"medium"`, or `"high"`.  
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
