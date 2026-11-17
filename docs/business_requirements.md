# Business Requirements Document (BRD)
## 1. Background
A fictional bank receives transaction and balance data from multiple core banking systems. Differences in formats and data quality can delay downstream accounting and financial reporting.

## 2. Business objective
Create a learning prototype that consolidates synthetic CASA, term-deposit and loan data; validates and standardises records; simulates event-to-account mapping; and highlights source-to-GL balance differences.

## 3. Stakeholders
- Finance Operations: reviews accounting output and reconciliation exceptions.
- Business/Product Operations: owns product and transaction definitions.
- Data Operations: supplies source files and resolves data quality issues.
- Functional Analyst: documents requirements, mappings, rules and test evidence.
- Technology/Development: implements the prototype and supports defect resolution.

## 4. Scope
### In scope
- CSV ingestion for CASA, term deposits, loans and balance snapshots.
- Required-field, duplicate, amount, date, currency and branch checks.
- Common transaction data model.
- Illustrative event-to-account mapping.
- Simulated balanced journal generation.
- Source-vs-GL balance comparison.
- Dashboard metrics and exception downloads.

### Out of scope
- Connection to Oracle AFCS, Oracle ERP, GL or live banking systems.
- Production accounting policy configuration or regulatory reporting.
- Real customer data, authentication, approvals or production-grade audit controls.
- Claiming equivalence with Oracle product internals.

## 5. Business requirements
- BR-01: Users shall be able to load synthetic source transaction files.
- BR-02: Users shall be able to identify invalid and duplicate records.
- BR-03: Users shall be able to view standardised records across source systems.
- BR-04: Users shall be able to inspect illustrative event-to-account mappings.
- BR-05: Users shall be able to generate balanced debit/credit journal simulations for valid mapped transactions.
- BR-06: Users shall be able to compare source and GL balances and identify differences.
- BR-07: Users shall be able to monitor processing counts, failures and reconciliation status.
- BR-08: Users shall be able to download exception and processing outputs.

## 6. Success criteria
- All source files load with a visible record count.
- Known seeded data quality exceptions are detected.
- Every generated journal has equal debit and credit totals.
- Reconciliation output flags the deliberately seeded balance mismatch.
- Users can export exception and reconciliation results.
