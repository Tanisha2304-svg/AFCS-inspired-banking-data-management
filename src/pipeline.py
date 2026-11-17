from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
REF = ROOT / "data" / "reference"
PROCESSED = ROOT / "data" / "processed"
PROCESSED.mkdir(parents=True, exist_ok=True)

FILES = ["casa_transactions.csv", "term_deposit_transactions.csv", "loan_transactions.csv"]

def load_transactions():
    frames = [pd.read_csv(RAW / f) for f in FILES]
    return pd.concat(frames, ignore_index=True)

def validate_transactions(df):
    out = df.copy()
    out["dq_errors"] = ""
    checks = {
        "transaction_id": out["transaction_id"].isna() | (out["transaction_id"].astype(str).str.strip() == ""),
        "customer_id": out["customer_id"].isna() | (out["customer_id"].astype(str).str.strip() == ""),
        "account_id": out["account_id"].isna() | (out["account_id"].astype(str).str.strip() == ""),
        "transaction_date": pd.to_datetime(out["transaction_date"], errors="coerce").isna(),
        "amount": pd.to_numeric(out["amount"], errors="coerce").isna() | (pd.to_numeric(out["amount"], errors="coerce") < 0),
    }
    for field, mask in checks.items():
        out.loc[mask, "dq_errors"] = out.loc[mask, "dq_errors"].apply(
            lambda x: (x + "; " if x else "") + f"Invalid {field}"
        )

    duplicate_mask = out.duplicated(["source_system", "transaction_id"], keep=False)
    out.loc[duplicate_mask, "dq_errors"] = out.loc[duplicate_mask, "dq_errors"].apply(
        lambda x: (x + "; " if x else "") + "Duplicate source_system + transaction_id"
    )

    branches = set(pd.read_csv(REF / "branch_reference.csv")["branch_code"].astype(str))
    currencies = set(pd.read_csv(REF / "currency_reference.csv")["currency_code"].astype(str))
    out.loc[~out["branch_code"].astype(str).isin(branches), "dq_errors"] = out.loc[
        ~out["branch_code"].astype(str).isin(branches), "dq_errors"
    ].apply(lambda x: (x + "; " if x else "") + "Unknown branch_code")
    out.loc[~out["currency"].astype(str).isin(currencies), "dq_errors"] = out.loc[
        ~out["currency"].astype(str).isin(currencies), "dq_errors"
    ].apply(lambda x: (x + "; " if x else "") + "Unknown currency")

    out["dq_status"] = out["dq_errors"].eq("").map({True: "VALID", False: "ERROR"})
    return out

def standardise(df):
    out = df.copy()
    for col in ["source_system", "event_type", "currency", "branch_code"]:
        out[col] = out[col].astype(str).str.strip().str.upper()
    out["transaction_date"] = pd.to_datetime(out["transaction_date"], errors="coerce")
    out["amount"] = pd.to_numeric(out["amount"], errors="coerce")
    return out

def generate_journals(valid_df):
    rules = pd.read_csv(REF / "event_accounting_rules.csv")
    merged = valid_df.merge(rules, on=["source_system", "event_type"], how="left")
    merged = merged.dropna(subset=["debit_account", "credit_account"]).copy()
    debit = merged[["transaction_id", "transaction_date", "currency", "debit_account", "amount"]].copy()
    debit.columns = ["transaction_id", "transaction_date", "currency", "account", "debit"]
    debit["credit"] = 0.0
    credit = merged[["transaction_id", "transaction_date", "currency", "credit_account", "amount"]].copy()
    credit.columns = ["transaction_id", "transaction_date", "currency", "account", "credit"]
    credit["debit"] = 0.0
    journals = pd.concat([debit, credit], ignore_index=True)
    return journals[["transaction_id", "transaction_date", "currency", "account", "debit", "credit"]]

def reconcile():
    src = pd.read_csv(RAW / "source_balances.csv")
    gl = pd.read_csv(RAW / "gl_balances.csv")
    result = src.merge(gl, on=["account_id", "as_of_date", "currency"], how="outer")
    result["difference"] = result["source_balance"].fillna(0) - result["gl_balance"].fillna(0)
    result["status"] = result["difference"].abs().le(0.01).map({True: "MATCH", False: "BREAK"})
    return result
