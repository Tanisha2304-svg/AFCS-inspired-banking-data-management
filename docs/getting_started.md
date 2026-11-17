# Getting Started — Session 1

## Step 1: Understand the business case
A fictional bank consolidates transaction and balance data from CASA, term-deposit and loan systems. The prototype checks quality, standardises data, simulates accounting mappings and identifies source-to-GL differences.

## Step 2: Inspect the files
Open the CSVs in `data/raw/` and `data/reference/`. All records are synthetic. Some transaction rows intentionally contain data-quality issues. The source and GL balance files contain a deliberately seeded mismatch for account A1002.

## Step 3: Read the requirements
Read `docs/business_requirements.md`, then `docs/functional_requirements.md`. The BRD explains why the business needs the process; the FRD explains what the system must do and how acceptance will be tested.

## Step 4: Run the prototype
Install dependencies and run:
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Step 5: Verify expected outcomes
- The DQ tab should flag the missing customer ID, negative amount, invalid branch and duplicate transaction key.
- The journal simulation should create debit and credit lines for valid records with configured event mappings.
- Reconciliation should flag account A1002 with a difference of INR 2,000.

## Step 6: Your functional consultant exercise
For each flagged record, document:
1. Requirement or business rule.
2. Input record and expected result.
3. Actual result.
4. Defect or exception description.
5. Severity and business impact.
6. Proposed resolution and retest result.

Do not change the source file to hide an exception. Record the original issue, then create a corrected copy or adjustment and show the retest.
