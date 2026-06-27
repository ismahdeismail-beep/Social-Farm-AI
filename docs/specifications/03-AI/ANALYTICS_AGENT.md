# Analytics Agent Specification

## 1. Purpose
The Analytics Agent is responsible for processing raw platform data, generating insights, and recommending growth strategies.

## 2. Responsibilities
*   Analyze content performance metrics.
*   Identify audience engagement patterns.
*   Generate actionable growth recommendations.
*   Provide sentiment analysis on audience feedback.

## 3. Workflow

```mermaid
graph LR
    Data[Raw Data] --> Processor[Data Processor]
    Processor --> Analyzer[Analytics Agent]
    Analyzer --> Insights[Insights Database]
    Insights --> Dashboard[Analytics Dashboard]
```

## 4. Key Metrics
*   Engagement Rate
*   Reach & Impressions
*   Conversion Rate
*   Audience Sentiment Score

## 5. Integration
*   **Input**: Data from Publishing Center and external platform APIs.
*   **Output**: JSON-formatted insights stored in the Analytics database.
