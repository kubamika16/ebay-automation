# eBay Undervalued iPhone Detector (Ebay Automation)

This project is designed to automate the detection of potentially undervalued iPhones listed on eBay. It integrates eBay’s API with AI-powered item analysis to notify users when good deals appear.

## Project Overview
The app uses predefined pricing rules and GPT-based analysis to identify undervalued iPhones listed on eBay. The system operates on a serverless AWS Lambda function that runs every 5 minutes, ensuring real-time monitoring and notifications.

## How It Works

1. **Data Collection**:
   - The app makes periodic API calls to eBay, filtering items based on price, listing time, and specific iPhone models. 
   - A dictionary of pre-configured models and price ranges is used, allowing for easy scalability.

2. **AI-Powered Condition Analysis**:
   - GPT is integrated to analyze the **title** and **description** of each listing. It helps verify the item's condition, ensuring only well-maintained items are flagged for notification.

3. **Real-Time Notifications**:
   - When an undervalued iPhone in good condition is detected, the app sends out real-time notifications to alert the user.

## Technologies Used
- **AWS Lambda**: Serverless function for executing tasks every 5 minutes.
- **eBay API**: To search and filter iPhone listings.
- **OpenAI (GPT)**: For analyzing item descriptions to determine item conditions.
- **GitHub Actions**: Used for CI/CD to automatically update the Lambda function when new code is committed.

## Continuous Deployment and Automation
The project is set up with a CI/CD pipeline that automatically deploys changes from GitHub to AWS Lambda. The Lambda function is scheduled to run every 5 minutes via a cron job, ensuring up-to-date item listings.

## Purpose
This project showcases my ability to integrate cloud-based services, APIs, and AI models to create real-time automated systems. It demonstrates skills in serverless architecture, automation, and AI-based decision-making.

---

### Why This Structure Works:
- **General and Future-Proof**: By avoiding specific details like iPhone models and condition categories, the `README.md` remains adaptable to future changes in the app.
- **Highlighting Key Skills**: It focuses on the technologies and workflow, which is ideal for a portfolio project.
- **No Installation Focus**: Since you’re not expecting others to use it, keeping out specific installation instructions keeps the focus on your skills and the purpose of the project.
