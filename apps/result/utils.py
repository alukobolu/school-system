def score_grade(score):
    # print(score)
    if score >= 70:
        return "A"
    elif score >= 60 and score < 70:
        return "B"
    elif score >= 50 and score < 60:
        return "C"
    elif score >= 40 and score < 50:
        return "D"
    elif score >= 30 and score < 40:
        return "E"
    elif score >= 0 and score < 30:
        return "F"
    else:
        return "N/A"