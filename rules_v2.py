"""EAS 510 - Project 1 - Phase 2: the V2 rule set.

Rules 1-3 are kept exactly as in `rules.py`. Your job is to ADD Rule 4 that
targets the systematic weakness you diagnosed from results_v1_hard.txt.

Constraint: the rules' `out_of` weights must still sum to 100 so the Final
Score stays on a /100 scale (the format validator enforces "Final Score:
<s>/100" equals the sum of the block's rule scores).

Example split that keeps the original spirit: Rules 1-3 -> 25/25/40 and
Rule 4 -> 10 (or trim the losers more aggressively).
"""

import rules

#: Import the original rules and append your new one.
RULES = rules.RULES + ("rule4_edges",)


def rule4_edges(target, input_path):
    """TODO: replace with your Phase 2 rule that fixes the V1 weakness.

    Starter returns a no-op so the pipeline still runs before you implement it.
    Parity with rules.py rule dict: rule/name/fired/score/out_of/note/metric.
    """

    try:
        out = {"rule": 4, "name": "Edges", "fired": False, "score": 0,
           "out_of": 10, "note": "Match score 0.00", "metric": 0.0}

        src_g = _gray(target["path"])
        nd_g = _gray(input_path)
        if src_g is None or nd_g is None:
            return out

        nd_g = cv2.resize(nd_g, (src_g.shape[1], src_g.shape[0]))


        src_edges = cv2.Canny(src_g, 50, 100)
        nd_edges = cv2.Canny(nd_g, 50, 100)

        kernel = np.ones((3,3),np.uint8)

        src_dilated = cv2.dilate(src_edges, kernel)
        nd_dilated = cv2.dilate(nd_edges, kernel)

        src_count = np.count_nonzero(src_edges)
        nd_count = np.count_nonzero(nd_edges)

        if src_count == 0 or nd_count == 0:
            return out

        src_matched = np.count_nonzero(
            (src_edges > 0) & (nd_dilated > 0)
        )

        nd_matched = np.count_nonzero(
            (nd_edges > 0) & (src_dilated > 0)
        )

        metric = 0.5 * (
            src_matched / src_count +
            nd_matched / nd_count
        )


       
        out["metric"] = round(max(0.0, min(1.0, metric)), 3)
        out["note"] = f"Edge matching {out['metric']:.2f}"

        if out["metric"] >= 0.2:
            out["fired"] = True
            out["score"] = int(round(10 * out["metric"]))

    except Exception:
        pass
    return out
