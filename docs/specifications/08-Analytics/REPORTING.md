# REPORTING

## Purpose
The reporting module facilitates scheduled and ad-hoc data distribution for stakeholders who require deeper analysis or offline access.

## Features
- **Scheduled Reports:** Daily, weekly, or monthly summaries delivered via email or webhook.
- **Ad-hoc Reporting:** A report builder interface to allow custom data exploration.
- **Exporting:** Support for [EXPORTS](./EXPORTS.md) (CSV, PDF, Excel).
- **Sharing:** Secure, permissioned sharing of reports within the organization.

## Implementation
Reports are generated using the data stored in the [DATA_PIPELINE](./DATA_PIPELINE.md) warehouse. Templates are versioned to ensure report consistency over time.
