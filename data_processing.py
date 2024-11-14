import pandas as pd


def calculate_scores(answers):
    # Convert answers to numeric values
    numeric_answers = [int(answer) for answer in answers]

    # Calculate average score
    average_score = sum(numeric_answers) / len(numeric_answers)

    # Calculate scores for different categories
    categories = ["Policy", "Data Governance", "Strategy", "AI Capabilities", "Ethics"]
    category_scores = {
        cat: sum(numeric_answers[i : i + 2]) / 2 for i, cat in enumerate(categories)
    }

    return average_score, category_scores


def prepare_radar_chart_data(category_scores):
    df = pd.DataFrame(list(category_scores.items()), columns=["Category", "Score"])
    df["Angle"] = [0, 2 * 3.14 / 3, 4 * 3.14 / 3]
    return df
