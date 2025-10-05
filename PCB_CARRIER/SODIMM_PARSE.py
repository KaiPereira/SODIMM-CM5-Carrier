import re
import sys
import csv
import os

def parse_kicad_sch(filename):
    with open(filename, "r", encoding="utf-8") as f:
        text = f.read()

    # Regex to capture global_label blocks
    blocks = re.findall(r"\(global_label\s+\"([^\"]+)\"(.*?)\)\s*\)", text, re.DOTALL)

    results = []
    for label, body in blocks:
        # Extract direction (shape)
        m = re.search(r"\(shape\s+(\w+)\)", body)
        direction = m.group(1) if m else "unknown"

        # Clean up KiCad-style escape sequences like {slash}
        clean_label = label.replace("{slash}", "/")

        # Filter out power symbols and NC
        if "NC" in clean_label.upper() or "NOCONNECT" in clean_label.upper():
            continue
        if any(pwr in clean_label.upper() for pwr in ["VCC", "GND", "3V3", "1V8", "1.8V", "3.3V", "5V", "VBAT"]):
            continue

        results.append((clean_label, clean_label, direction))

    return results


def main():
    if len(sys.argv) < 2:
        print("Usage: python parse_sodimm.py file.kicad_sch")
        sys.exit(1)

    infile = sys.argv[1]
    outfile = os.path.splitext(infile)[0] + "_pinout.csv"

    pinout = parse_kicad_sch(infile)

    with open(outfile, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Pin Name", "Name", "Direction"])
        writer.writerows(pinout)

    print(f"Pinout written to {outfile}")

if __name__ == "__main__":
    main()

