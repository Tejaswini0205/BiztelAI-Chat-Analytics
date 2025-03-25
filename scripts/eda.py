import json
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


class EDA:
    def __init__(self, file_path, save_dir="plots"):
        self.file_path = file_path
        self.df = None
        self.save_dir = save_dir

        # Create save directory if it doesn't exist
        os.makedirs(self.save_dir, exist_ok=True)

    def load_data(self):
        """Load and preprocess JSON dataset."""
        with open(self.file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Flatten the nested JSON structure
        conversations = []
        for conv_id, conv_data in data.items():
            for turn in conv_data.get("content", []):
                turn["conversation_id"] = conv_id  # Add conversation ID
                conversations.append(turn)

        self.df = pd.DataFrame(conversations)
        return self.df

    def basic_info(self):
        """Display basic info about the dataset."""
        print("Dataset Info:")
        print(self.df.info())
        print("\nFirst 5 Rows:")
        print(self.df.head())

    def sentiment_distribution(self):
        """Plot and save sentiment distribution."""
        plt.figure(figsize=(10, 5))
        sns.countplot(data=self.df, x="sentiment", order=self.df["sentiment"].value_counts().index)
        plt.xticks(rotation=45)
        plt.title("Sentiment Distribution")
        plt.xlabel("Sentiment")
        plt.ylabel("Count")
        plt.savefig(os.path.join(self.save_dir, "sentiment_distribution.png"))
        plt.close()  # Close plot to free memory

    def agent_analysis(self):
        """Plot and save message count per agent."""
        plt.figure(figsize=(10, 5))
        sns.countplot(data=self.df, x="agent", order=self.df["agent"].value_counts().index)
        plt.title("Message Count per Agent")
        plt.xlabel("Agent")
        plt.ylabel("Message Count")
        plt.savefig(os.path.join(self.save_dir, "agent_analysis.png"))
        plt.close()

    def show_summary(self):
        """Print summary statistics."""
        print("Unique Sentiments:", self.df["sentiment"].nunique())
        print("Sentiments:", self.df["sentiment"].unique())
        print("\nAgent Distribution:\n", self.df["agent"].value_counts())

    def run_all(self):
        """Run all EDA functions."""
        self.basic_info()
        self.show_summary()
        self.sentiment_distribution()
        self.agent_analysis()
        print(f"Plots saved in: {self.save_dir}/")


if __name__ == "__main__":
    file_path = "data/BiztelAI_DS_Dataset_Mar'25.json"
    eda = EDA(file_path)
    df = eda.load_data()
    eda.run_all()
