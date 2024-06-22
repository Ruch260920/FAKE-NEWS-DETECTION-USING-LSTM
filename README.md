# FAKE-NEWS-DETECTION-USING-LSTM

Overview
This project aims to detect fake news using a Long Short-Term Memory (LSTM) neural network. The model is trained on a dataset of news articles to distinguish between real and fake news based on textual features.

Table of Contents
Project Structure
Installation
Usage
Data Collection and Preprocessing
Model Training and Evaluation
Results
Visualization
Contributing
License
Project Structure
The project is organized into the following directories and files:

Fake_News_detection_lstm.py: Main script for the project.
README.md: Project documentation.
Installation
To set up the project on your local machine, follow these steps:

Clone the repository from GitHub.
Create and activate a virtual environment.
Install the required dependencies listed in requirements.txt.
Usage
To preprocess the data, train the model, and evaluate it, run the respective scripts located in the src directory. Alternatively, you can run the main script to see the entire workflow of the project.

Data Collection and Preprocessing
Data Collection: A dataset of news articles labeled as real or fake was collected from various sources.
Data Cleaning: The text data was processed to remove noise, handle punctuation, and convert to lowercase.
Tokenization: The text was tokenized into sequences suitable for training the LSTM model.
Model Training and Evaluation
Model: The project uses an LSTM neural network to learn patterns in the news articles and classify them as real or fake.
Training: The data was split into training and validation sets, and the model was trained using the training set.
Evaluation: The model's performance was evaluated using accuracy, precision, recall, and F1-score metrics. Fine-tuning was performed to improve the model's performance.
Results
The LSTM model successfully distinguished between real and fake news articles with high accuracy. An analysis of the model's predictions provided insights into its learning process and identified areas for improvement.

Visualization
Visualizations were created to track the training process and evaluate the model's performance. Training and validation loss were plotted over epochs to assess model convergence.
