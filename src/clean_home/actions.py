# TODO: Side effects (dry-run vs. real).
# def plan_moves(candidates, move_to) -> list[tuple[src, dst]]  # pure
# def perform_moves(plan) -> list[tuple[src, dst, ok_bool, error_str]]  # impure
#
# Create move_to if missing.
# Use shutil.move; ensure same-device vs cross-device moves handled by shutil.
