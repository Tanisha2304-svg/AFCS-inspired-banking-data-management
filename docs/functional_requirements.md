# Functional Requirements Document (FRD)
## 1. Functional overview
The prototype will execute a simplified flow: ingest → validate → standardise → map → generate journal simulation → reconcile → report.

## 2. Functional requirements
| ID | Requirement | Acceptance criteria |
|---|---|---|
| FR-01 | Load source CSV files | CASA, term-deposit and loan files load and display row counts |
| FR-02 | Validate mandatory fields | Missing transaction ID, account ID, customer ID, date, amount or currency is flagged |
| FR-03 | Detect duplicates | Duplicate source_system + transaction_id combinations are identified |
| FR-04 | Validate amount and date | Negative amounts and invalid dates are flagged |
| FR-05 | Validate reference values | Unknown currency and branch codes are flagged against reference files |
| FR-06 | Standardise data | All source files are combined into one common transaction schema |
| FR-07 | Apply illustrative accounting map | Valid event types map to configured debit and credit accounts |
| FR-08 | Generate journal simulation | Each valid mapped transaction creates debit and credit lines of equal value |
| FR-09 | Reconcile balances | Source and GL balances are compared by account, date and currency |
| FR-10 | Monitor processing | Dashboard displays loaded, valid, exception, journal and reconciliation counts |
| FR-11 | Export results | User can download exception, standardised, journal and reconciliation CSVs |

## 3. Non-functional requirements
- NFR-01: All data must be synthetic.
- NFR-02: Monetary values must be handled consistently and displayed with currency.
- NFR-03: Processing should be repeatable using the supplied files.
- NFR-04: The interface should clearly distinguish valid, warning and failed records.
- NFR-05: The prototype should not imply connection to Oracle AFCS or a production ledger.

## 4. Business rules
- A transaction is eligible for journal simulation only when it passes required DQ checks and has a matching event-accounting rule.
- Duplicate transaction keys are flagged; they are not silently deleted.
- A journal is balanced when total debits equal total credits for the transaction.
- Reconciliation difference = source balance − GL balance.
- Status is MATCH when absolute difference is within the configurable tolerance; otherwise BREAK.
- Currency must match before comparing balances. No FX conversion is implemented in this starter scope.

## 5. Assumptions and dependencies
- Reference data is illustrative and supplied locally as CSV.
- Debit/credit mappings are sample rules only and must not be treated as a bank-approved accounting policy.
- The project uses simplified one-to-one account reconciliation.
