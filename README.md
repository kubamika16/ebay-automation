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

## Push Notification Result

The project delivers notifications via the [Pushover](https://pushover.net/) service when a new undervalued item is found.

Here’s an example of the notification sent when the app identifies a match:
- **Item**: Apple iPhone 12 - 64GB - White (Unlocked)
- **Price**: £150 (which falls within the predefined undervalued price range of £110 - £150)
- **Link**: The notification includes a direct link to the eBay auction for quick access.

![Notification Example](path_to_your_image)
![Notification Message on Pushover App](path_to_your_image)
![Actual item (iPhone 12)](path_to_your_image)

This system ensures that fresh listings from the last 5 minutes are evaluated and flagged in real-time.

## Technologies Used
- **AWS Lambda**: Serverless function for executing tasks every 5 minutes.
- **eBay API**: To search and filter iPhone listings.
- **OpenAI (GPT)**: For analyzing item descriptions to determine item conditions.
- **Pushover**: For sending real-time push notifications.
- **GitHub Actions**: Used for CI/CD to automatically update the Lambda function when new code is committed.

## Continuous Deployment and Automation
The project is set up with a CI/CD pipeline that automatically deploys changes from GitHub to AWS Lambda. The Lambda function is scheduled to run every 5 minutes via a cron job, ensuring up-to-date item listings.

## Purpose
This project showcases my ability to integrate cloud-based services, APIs, and AI models to create real-time automated systems. It demonstrates skills in serverless architecture, automation, and AI-based decision-making.