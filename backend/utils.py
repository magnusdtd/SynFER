import sys


# Dummy classes for torch.load unpickler to succeed when loading POSTER++ checkpoints
class RecorderMeter:
    def __init__(self, *args, **kwargs):
        pass


class RecorderMeter1:
    def __init__(self, *args, **kwargs):
        pass


# Dynamic injection into __main__ namespace
main_module = sys.modules.get("__main__")
if main_module:
    if not hasattr(main_module, "RecorderMeter"):
        setattr(main_module, "RecorderMeter", RecorderMeter)
    if not hasattr(main_module, "RecorderMeter1"):
        setattr(main_module, "RecorderMeter1", RecorderMeter1)

# Facial Action Units order mapping as defined in OpenGraphAU MEFARG outputs
AU_IDS = [
    "1",
    "2",
    "4",
    "5",
    "6",
    "7",
    "9",
    "10",
    "11",
    "12",
    "13",
    "14",
    "15",
    "16",
    "17",
    "18",
    "19",
    "20",
    "22",
    "23",
    "24",
    "25",
    "26",
    "27",
    "32",
    "38",
    "39",
    "L1",
    "R1",
    "L2",
    "R2",
    "L4",
    "R4",
    "L6",
    "R6",
    "L10",
    "R10",
    "L12",
    "R12",
    "L14",
    "R14",
]


def make_au_vector(selected_aus: list[str]) -> list[float]:
    """
    Translates a list of select Action Units (e.g. ['AU6', 'AU12'])
    to the 41-dimensional binary vector layout required by the AU-Adapter.
    """
    vec = [0.0] * 41
    selected_upper = [au.upper() for au in selected_aus]
    for au in selected_upper:
        num = au.replace("AU", "")  # Extract number e.g., '6'
        for idx, au_id in enumerate(AU_IDS):
            if au_id == num:
                vec[idx] = 1.0
            elif au_id in (f"L{num}", f"R{num}"):
                vec[idx] = 1.0
    return vec


def determine_expression_category(prompt: str, selected_aus: list[str]) -> str:
    """
    Determines the target facial expression classification (matching POSTER++ labels)
    based on the text prompt keywords and manually toggled Action Units.
    """
    p_lower = prompt.lower()
    selected_lower = [a.lower() for a in selected_aus]

    # Check for Anger / angry
    if (
        "au4" in selected_lower
        or "au23" in selected_lower
        or "au24" in selected_lower
        or any(word in p_lower for word in ["angry", "anger", "frustrated", "mad", "furious"])
    ):
        return "Anger"
    # Check for happy
    if (
        "au12" in selected_lower
        or "au6" in selected_lower
        or any(word in p_lower for word in ["happy", "smile", "joy", "cheerful"])
    ):
        return "happy"
    # Check for sad
    if ("au1" in selected_lower and ("au15" in selected_lower or "au16" in selected_lower)) or any(
        word in p_lower for word in ["sad", "sadness", "cry", "grief", "depressed", "sorrow"]
    ):
        return "sad"
    # Check for surprise
    if (
        "au26" in selected_lower
        or "au27" in selected_lower
        or any(word in p_lower for word in ["surprise", "surprised", "astonish", "shock"])
    ):
        return "surprise"
    # Check for disgust
    if (
        "au9" in selected_lower
        or "au10" in selected_lower
        or any(word in p_lower for word in ["disgust", "gross", "yuck"])
    ):
        return "disgust"
    # Check for fear
    if "au20" in selected_lower or any(word in p_lower for word in ["fear", "scared", "afraid", "terror"]):
        return "fear"
    # Check for contempt
    if any(word in p_lower for word in ["contempt", "scorn", "disdain"]):
        return "Contempt"

    return "neutral"


def simulate_landmarks(expr: str, selected_aus: list[str]) -> dict:
    """
    Simulates coordinate-based landmarks scaled to a 400x400 space
    designed to draw vector coordinates over the canvas preview in Next.js.
    """
    base_landmarks = {
        "leftBrow": [{"x": 120, "y": 140}, {"x": 140, "y": 130}, {"x": 165, "y": 135}],
        "rightBrow": [{"x": 235, "y": 135}, {"x": 260, "y": 130}, {"x": 280, "y": 140}],
        "leftEye": [{"x": 135, "y": 165}, {"x": 150, "y": 158}, {"x": 165, "y": 165}, {"x": 150, "y": 172}],
        "rightEye": [{"x": 235, "y": 165}, {"x": 250, "y": 158}, {"x": 265, "y": 165}, {"x": 250, "y": 172}],
        "noseBridge": [{"x": 200, "y": 150}, {"x": 200, "y": 200}],
        "noseTip": [{"x": 185, "y": 220}, {"x": 200, "y": 225}, {"x": 215, "y": 220}],
        "mouthOuter": [
            {"x": 145, "y": 285},
            {"x": 175, "y": 275},
            {"x": 200, "y": 278},
            {"x": 225, "y": 275},
            {"x": 255, "y": 285},
            {"x": 225, "y": 305},
            {"x": 200, "y": 310},
            {"x": 175, "y": 305},
        ],
        "jaw": [
            {"x": 110, "y": 200},
            {"x": 115, "y": 250},
            {"x": 130, "y": 300},
            {"x": 160, "y": 345},
            {"x": 200, "y": 365},
            {"x": 240, "y": 345},
            {"x": 270, "y": 300},
            {"x": 285, "y": 250},
            {"x": 290, "y": 200},
        ],
    }

    selected_upper = [a.upper() for a in selected_aus]
    expr_lower = expr.lower()

    # FACS Mapping Adjustments:
    # AU12 (Lip Corner Puller / Smile)
    if "AU12" in selected_upper or expr_lower == "happy":
        base_landmarks["mouthOuter"][0]["x"] -= 8
        base_landmarks["mouthOuter"][0]["y"] -= 10
        base_landmarks["mouthOuter"][4]["x"] += 8
        base_landmarks["mouthOuter"][4]["y"] -= 10
        base_landmarks["mouthOuter"][6]["y"] += 5
        base_landmarks["mouthOuter"][2]["y"] -= 4

    # AU15 (Lip Corner Depressor / Frown)
    if "AU15" in selected_upper or expr_lower == "sad":
        base_landmarks["mouthOuter"][0]["y"] += 12
        base_landmarks["mouthOuter"][4]["y"] += 12
        base_landmarks["mouthOuter"][2]["y"] -= 6

    # AU1 (Inner Brow Raiser)
    if "AU1" in selected_upper or expr_lower in ["sad", "surprise"]:
        base_landmarks["leftBrow"][2]["y"] -= 15
        base_landmarks["rightBrow"][0]["y"] -= 15

    # AU4 (Brow Lowerer)
    if "AU4" in selected_upper or expr_lower == "angry":
        base_landmarks["leftBrow"][0]["y"] += 8
        base_landmarks["leftBrow"][2]["y"] += 12
        base_landmarks["leftBrow"][2]["x"] += 5
        base_landmarks["rightBrow"][0]["y"] += 12
        base_landmarks["rightBrow"][0]["x"] -= 5
        base_landmarks["rightBrow"][2]["y"] += 8

    # AU5 (Upper Lid Raiser)
    if "AU5" in selected_upper or expr_lower in ["surprise", "fear"]:
        base_landmarks["leftEye"][1]["y"] -= 8
        base_landmarks["rightEye"][1]["y"] -= 8

    # AU26/AU27 (Jaw Drop / Mouth Stretch)
    if "AU26" in selected_upper or "AU27" in selected_upper or expr_lower == "surprise":
        mouth_down = 25 if "AU27" in selected_upper else 15
        base_landmarks["mouthOuter"][5]["y"] += mouth_down
        base_landmarks["mouthOuter"][6]["y"] += mouth_down + 5
        base_landmarks["mouthOuter"][7]["y"] += mouth_down
        base_landmarks["jaw"][4]["y"] += int(mouth_down * 0.8)
        base_landmarks["jaw"][3]["y"] += int(mouth_down * 0.6)
        base_landmarks["jaw"][5]["y"] += int(mouth_down * 0.6)

    return base_landmarks
