MILESTONES = [250, 500, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 10000, 15000, 20000]


def get_milestone_data(current_total: float) -> dict:
    """
    Given the current donation total, calculate milestone progress.
    Returns next_target, progress_percent, and remaining_to_target.
    """
    next_target = None
    for milestone in MILESTONES:
        if current_total < milestone:
            next_target = milestone
            break

    # If we've exceeded all milestones, use the last one as reference
    if next_target is None:
        next_target = MILESTONES[-1]
        progress_percent = 100.0
        remaining = 0.0
    else:
        # Find the previous milestone (or 0 if before first)
        idx = MILESTONES.index(next_target)
        prev_target = MILESTONES[idx - 1] if idx > 0 else 0

        range_size = next_target - prev_target
        progress_in_range = current_total - prev_target
        progress_percent = round((progress_in_range / range_size) * 100, 2)
        remaining = round(next_target - current_total, 2)

    return {
        "current_total": current_total,
        "next_target": next_target,
        "progress_percent": progress_percent,
        "remaining": remaining,
    }
