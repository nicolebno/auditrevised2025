# Premium Comparison Audit Tool

This Streamlit app allows users to compare employee census data against carrier invoice data to identify mismatches or missing premium information.

---

### 🚀 Features

- Upload a **Census File** and a **Carrier Invoice File**
- Automatically compares:
  - First and Last Names
  - Total Premium vs. Carrier Premium
- Flags mismatches or missing values
- Download results as a CSV
- Download templates to ensure correct formatting

---

### 📂 File Templates

Download the required templates from the app or this repo:

- `Census Audit Template.xlsx`
- `Carrier Invoice Audit Template.xlsx`

These templates ensure columns are formatted correctly:
- Census: `FIRST NAME`, `LAST NAME`, `TOTAL PREMIUM`
- Carrier: `FIRST NAME`, `LAST NAME`, `CARRIER PREMIUM`

---

### 📦 Requirements

Install dependencies:
```bash
pip install -r requirements.txt
