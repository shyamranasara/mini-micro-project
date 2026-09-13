# 🗳️ Electoral Bonds Data Analytics

An interactive data analysis and visualization module exploring Indian Electoral Bonds data. This project links bond purchases made by corporate entities and individuals directly to encashment records by political parties.

## 📌 Overview
- **Objective**: Analyze financial flow, top donor companies, receiving political parties, and denomination breakdown.
- **Dataset**: `Company.csv`, `Party.csv`, and pre-merged bond linkage dataset `df.csv`.
- **Key Metric**: Total donation value in ₹ Crores (INR).

## 🚀 Key Features
- **Political Party Breakdown**: Ranking political parties by total encashed funds.
- **Top Purchaser Identification**: Identifying top corporate donors and bond buyer groups.
- **Donor-to-Party Linkage**: Interactive drill-down into specific corporate contributions to individual political parties.
- **Searchable Database**: Real-time search across purchasers, parties, and bond denominations.

## 🛠️ How to Run Standalone
```bash
streamlit run "Election Bonds/app.py"
```

## 📊 Dataset Structure
| Column Name | Description |
|---|---|
| `Date of Purchase` | Date when electoral bond was purchased |
| `Name of the Purchaser` | Entity or corporate company purchasing the bond |
| `Bond Number` | Unique identifying number linking purchase to encashment |
| `Denominations` | Face value of the bond in INR |
| `Name of the Political Party` | Political party that encashed the bond |
