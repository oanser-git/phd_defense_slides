from pathlib import Path
import subprocess
import xml.etree.ElementTree as ET


SVG_NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG_NS)

SOURCE = Path(__file__).with_name("ml_prediction_task_diagram.svg")

FADED_OPACITY = "0.14"
DIMMED_OPACITY = "0.35"


def qname(tag: str) -> str:
    return f"{{{SVG_NS}}}{tag}"


def matches_text(elem: ET.Element, content: str) -> bool:
    return elem.tag == qname("text") and (elem.text or "").strip() == content


def matches_rect(elem: ET.Element, x: str, y: str) -> bool:
    return elem.tag == qname("rect") and elem.get("x") == x and elem.get("y") == y


def matches_path(elem: ET.Element, prefix: str) -> bool:
    return elem.tag == qname("path") and (elem.get("d") or "").startswith(prefix)


def classify_groups(root: ET.Element) -> dict[str, list[ET.Element]]:
    groups = {
        "network": [],
        "feature": [],
        "detection": [],
        "classification": [],
        "anomaly": [],
    }

    for elem in root.findall(qname("*")):
        if matches_rect(elem, "30", "150") or matches_text(elem, "Network observation") or matches_rect(elem, "70", "240") or matches_text(elem, "packet") or matches_rect(elem, "225", "240") or matches_text(elem, "flow") or matches_rect(elem, "70", "308") or matches_text(elem, "sequence") or matches_rect(elem, "225", "308") or matches_text(elem, "graph"):
            groups["network"].append(elem)
        elif matches_rect(elem, "470", "175") or matches_text(elem, "Feature representation") or matches_text(elem, "turn traffic into numerical features") or matches_text(elem, "for the model to process") or matches_text(elem, "duration | bytes | packets | destination port") or matches_path(elem, "M410 270 H455"):
            groups["feature"].append(elem)
        elif matches_rect(elem, "1010", "175") or matches_text(elem, "Detection model") or matches_text(elem, "ML / DL model") or matches_text(elem, "RF, AE, CNN, GNN, ...") or matches_path(elem, "M910 270 H995"):
            groups["detection"].append(elem)
        elif matches_text(elem, "Two common learning settings") or matches_rect(elem, "1470", "85") or matches_text(elem, "Classification") or matches_text(elem, "trained on labeled") or matches_text(elem, "benign + attack traffic") or matches_text(elem, "output: traffic label") or matches_rect(elem, "1498", "266") or matches_text(elem, "benign") or matches_rect(elem, "1604", "266") or matches_text(elem, "DDoS") or matches_rect(elem, "1700", "266") or matches_text(elem, "botnet") or matches_path(elem, "M1350 255 C1410 255"):
            groups["classification"].append(elem)
        elif matches_rect(elem, "1470", "365") or matches_text(elem, "Anomaly detection") or matches_text(elem, "trained mainly on") or matches_text(elem, "benign traffic") or matches_text(elem, "output: score -> alert") or matches_rect(elem, "1578", "548") or matches_text(elem, "score > τ") or matches_path(elem, "M1350 295 C1410 295"):
            groups["anomaly"].append(elem)

    return groups


def set_group_opacity(groups: dict[str, list[ET.Element]], opacities: dict[str, str]) -> None:
    for group_name, elems in groups.items():
        opacity = opacities[group_name]
        for elem in elems:
            elem.set("opacity", opacity)


def export_stage(stage_name: str, opacities: dict[str, str]) -> None:
    tree = ET.parse(SOURCE)
    root = tree.getroot()
    groups = classify_groups(root)
    set_group_opacity(groups, opacities)

    svg_path = SOURCE.with_name(f"ml_prediction_task_diagram_{stage_name}.svg")
    pdf_path = SOURCE.with_name(f"ml_prediction_task_diagram_{stage_name}.pdf")
    png_path = SOURCE.with_name(f"ml_prediction_task_diagram_{stage_name}.png")

    tree.write(svg_path, encoding="utf-8", xml_declaration=True)
    subprocess.run(["rsvg-convert", "-f", "pdf", "-o", str(pdf_path), str(svg_path)], check=True)
    subprocess.run(["rsvg-convert", "-f", "png", "-o", str(png_path), str(svg_path)], check=True)


def main() -> None:
    export_stage(
        "stage1",
        {
            "network": "1",
            "feature": FADED_OPACITY,
            "detection": FADED_OPACITY,
            "classification": FADED_OPACITY,
            "anomaly": FADED_OPACITY,
        },
    )
    export_stage(
        "stage2",
        {
            "network": "1",
            "feature": "1",
            "detection": FADED_OPACITY,
            "classification": FADED_OPACITY,
            "anomaly": FADED_OPACITY,
        },
    )
    export_stage(
        "stage3",
        {
            "network": "1",
            "feature": "1",
            "detection": "1",
            "classification": FADED_OPACITY,
            "anomaly": FADED_OPACITY,
        },
    )
    export_stage(
        "stage4",
        {
            "network": "1",
            "feature": "1",
            "detection": "1",
            "classification": "1",
            "anomaly": FADED_OPACITY,
        },
    )
    export_stage(
        "stage5",
        {
            "network": "1",
            "feature": "1",
            "detection": "1",
            "classification": "1",
            "anomaly": "1",
        },
    )


if __name__ == "__main__":
    main()
