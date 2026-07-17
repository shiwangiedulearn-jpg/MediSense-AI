import re


def extract_liver_values(text):

    values = {
        "tot_bilirubin": 0,
        "direct_bilirubin": 0,
        "tot_proteins": 0,
        "albumin": 0,
        "ag_ratio": 0,
        "sgpt": 0,
        "sgot": 0,
        "alkphos": 0
    }

    lines = text.split("\n")

    for line in lines:

        line_lower = line.lower()

        numbers = re.findall(r"\d+\.?\d*", line)

        if not numbers:
            continue

        value = float(numbers[0])

       
        if (
            "total bilirubin" in line_lower
            or "tot bilirubin" in line_lower
        ):

            values["tot_bilirubin"] = value

       
        elif (
            "direct bilirubin" in line_lower
            or "conjugated bilirubin" in line_lower
        ):

            values["direct_bilirubin"] = value

    
        elif (
            "sgpt" in line_lower
            or "alt" in line_lower
            or "alanine aminotransferase" in line_lower
        ):

            values["sgpt"] = value

      
        elif (
            "sgot" in line_lower
            or "ast" in line_lower
            or "aspartate aminotransferase" in line_lower
        ):

            values["sgot"] = value

       
        elif (
            "alkaline phosphatase" in line_lower
            or "alkphos" in line_lower
            or "alp" in line_lower
        ):

            values["alkphos"] = value

       
        elif (
            "total protein" in line_lower
            or "total proteins" in line_lower
        ):

            values["tot_proteins"] = value

     
        elif "albumin" in line_lower and "globulin" not in line_lower:

            values["albumin"] = value

      
        elif (
            "albumin globulin ratio" in line_lower
            or "a/g ratio" in line_lower
            or "ag ratio" in line_lower
        ):

            values["ag_ratio"] = value

    return values