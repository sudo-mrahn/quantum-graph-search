"""Internal compatibility helpers for legacy quantum-walk sampling APIs."""

from qw._localization import sample_localization_series


def sample_localization_measure_series(
    adj_mat,
    marked_node_indices,
    initial,
    maxss,
    total_steps,
    *,
    walk_step_fn,
    measure_fn,
):
    """
    Run the historical multi-marked-node localization workflow.
    """

    return sample_localization_series(
        adj_mat,
        marked_node_indices,
        initial,
        maxss,
        total_steps,
        walk_step_fn=walk_step_fn,
        measure_fn=measure_fn,
    )
