"""Exact thirteen-block dominant Gram on a finite target tail band."""

from __future__ import annotations

import hashlib
import json
import math
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from experiments.theta_pencil.arb_adjacent_full_map import (
    _build_adjacent_full_matrix,
    _build_separated_full_matrix,
)
from experiments.theta_pencil.arb_cut_smooth import _power_block_rectangular
from experiments.theta_pencil.arb_prime_translation import _arb_radius_as_float
from experiments.theta_pencil.arb_source_schur import _roundtrip_ball
from experiments.theta_pencil.arb_third_window_source import (
    _arb_breakpoints_lengths,
    _degree_pattern,
    _offsets,
    _parity_transforms,
)
from experiments.theta_pencil.cut_adapted_prime_basis import third_prime_partition
from experiments.theta_pencil.smooth_legendre_series import (
    smooth_remainder_series_coefficients,
)


@dataclass(frozen=True)
class ArbThirdWindowNearTailGram:
    even_midpoint: np.ndarray
    even_radius: np.ndarray
    odd_midpoint: np.ndarray
    odd_radius: np.ndarray
    interval_degrees: tuple[int, ...]
    first_degree: int
    last_degree: int
    precision: int
    working_precision: int
    maximum_smooth_power: int | None


def _export(matrix):
    midpoint = np.empty((matrix.nrows(), matrix.ncols()), dtype=float)
    radius = np.empty_like(midpoint)
    for row in range(matrix.nrows()):
        for column in range(matrix.ncols()):
            midpoint[row, column] = float(matrix[row, column].mid())
            radius[row, column] = _arb_radius_as_float(matrix[row, column])
    return midpoint, radius


def _cross_map_cache_metadata(
    half_width: float,
    target_label: str,
    source_label: str,
    gap_signature: tuple[int, int, int],
    source_degree_count: int,
    first_degree: int,
    last_degree: int,
    working_precision: int,
    builder_kind: str,
) -> dict[str, int | str | list[int]]:
    """Describe every proof-relevant input to one reusable cross map."""

    return {
        "format": 1,
        "architecture": "third-window-near-tail-cross-map",
        "half_width": repr(half_width),
        "target_label": target_label,
        "source_label": source_label,
        "gap_signature": list(gap_signature),
        "source_degree_count": source_degree_count,
        "first_degree": first_degree,
        "last_degree": last_degree,
        "working_precision": working_precision,
        "builder_kind": builder_kind,
    }


def _smooth_map_cache_metadata(
    half_width: float,
    target_label: str,
    source_label: str,
    gap_signature: tuple[int, int, int],
    source_degree_count: int,
    smooth_degree: int,
    maximum_smooth_power: int,
    precision: int,
    same_block: bool,
) -> dict[str, int | str | bool | list[int]]:
    return {
        "format": 1,
        "architecture": "third-window-near-tail-smooth-map",
        "half_width": repr(half_width),
        "target_label": target_label,
        "source_label": source_label,
        "gap_signature": list(gap_signature),
        "source_degree_count": source_degree_count,
        "smooth_degree": smooth_degree,
        "maximum_smooth_power": maximum_smooth_power,
        "precision": precision,
        "same_block": same_block,
    }


def _matrix_cache_path(
    cache_directory: str | Path,
    metadata,
    prefix: str,
) -> Path:
    encoded = json.dumps(metadata, sort_keys=True, separators=(",", ":"))
    digest = hashlib.sha256(encoded.encode("utf-8")).hexdigest()[:24]
    return Path(cache_directory) / f"{prefix}-{digest}.npz"


def _save_arb_matrix(path: Path, matrix, metadata) -> None:
    """Atomically store parseable Arb balls, preserving tiny coefficients."""

    path.parent.mkdir(parents=True, exist_ok=True)
    balls = np.array(
        [
            [matrix[row, column].str(more=True) for column in range(matrix.ncols())]
            for row in range(matrix.nrows())
        ]
    )
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("wb") as stream:
        np.savez_compressed(
            stream,
            metadata=np.array(json.dumps(metadata, sort_keys=True)),
            balls=balls,
        )
    temporary.replace(path)


def _load_arb_matrix(path: Path, expected_metadata, arb, arb_mat):
    """Reload one map only when all proof parameters agree exactly."""

    if not path.exists():
        return None
    with np.load(path, allow_pickle=False) as payload:
        metadata = json.loads(str(payload["metadata"].item()))
        if metadata != expected_metadata:
            raise ValueError("the Arb-matrix cache metadata do not match")
        balls = payload["balls"]
    if "smooth_degree" in metadata:
        row_count = int(metadata["smooth_degree"])
    else:
        row_count = int(metadata["last_degree"]) - int(
            metadata["first_degree"]
        )
    expected_shape = (row_count, int(metadata["source_degree_count"]))
    if balls.shape != expected_shape:
        raise ValueError("the Arb-matrix cache shape does not match its metadata")
    matrix = arb_mat(*expected_shape)
    for row in range(expected_shape[0]):
        for column in range(expected_shape[1]):
            # The saved string is itself an enclosing Arb interval.  Parsing
            # it at the registered working precision preserves that inclusion.
            matrix[row, column] = arb(str(balls[row, column]))
    return matrix


def build_arb_third_window_near_tail_gram(
    half_width: float = 0.7,
    edge_degree: int = 16,
    bridge_degree: int = 16,
    center_degree: int = 16,
    first_degree: int = 16,
    last_degree: int = 640,
    precision: int = 512,
    maximum_smooth_power: int | None = 47,
    band_boundaries: tuple[int, ...] | None = None,
    cross_map_cache_dir: str | Path | None = None,
) -> ArbThirdWindowNearTailGram | tuple[ArbThirdWindowNearTailGram, ...]:
    """Accumulate every source contribution in each exact target row."""

    third_prime_partition(half_width)
    degrees = _degree_pattern(edge_degree, bridge_degree, center_degree)
    if first_degree < max(degrees) or last_degree <= first_degree:
        raise ValueError("the explicit band must start above all source modes")
    if maximum_smooth_power is not None and maximum_smooth_power < 1:
        raise ValueError("maximum_smooth_power must be positive")
    boundaries = band_boundaries or (first_degree, last_degree)
    if (
        len(boundaries) < 2
        or boundaries[0] != first_degree
        or boundaries[-1] != last_degree
        or any(right <= left for left, right in zip(boundaries[:-1], boundaries[1:]))
    ):
        raise ValueError(
            "band_boundaries must strictly partition the explicit band"
        )
    try:
        from flint import acb, arb, arb_mat, ctx
    except ImportError as error:  # pragma: no cover
        raise RuntimeError("python-flint is required") from error

    labels = (
        "edge",
        "bridge",
        "edge",
        "center",
        "edge",
        "bridge",
        "edge",
        "bridge",
        "edge",
        "center",
        "edge",
        "bridge",
        "edge",
    )
    previous_precision = ctx.prec
    try:
        ctx.prec = max(precision, 128)
        _, _, pilot_lengths = _arb_breakpoints_lengths(arb, half_width)
        eta_candidates = []
        for target in range(13):
            for source in range(13):
                if source == target:
                    continue
                lower = min(target, source)
                upper = max(target, source)
                gap = sum(pilot_lengths[lower + 1 : upper], arb(0))
                eta_candidates.append(
                    (
                        1
                        + 2
                        * (gap + pilot_lengths[source])
                        / pilot_lengths[target]
                    ).acosh()
                )
        maximum_eta = max(float(value.upper()) for value in eta_candidates)
        working_precision = max(
            precision,
            math.ceil(
                (last_degree + max(degrees) + 2)
                * maximum_eta
                / math.log(2)
            )
            + precision
            + 128,
        )

        smooth_maps = None
        smooth_degree = 0
        if maximum_smooth_power is not None:
            # Only requested target rows are needed.  The former unconditional
            # ``p + d + 2`` build was correct but made a four-row prefix pay
            # for dozens of unused polynomial rows.
            smooth_degree = min(
                last_degree, maximum_smooth_power + max(degrees) + 2
            )
            coefficients = smooth_remainder_series_coefficients(
                maximum_smooth_power
            )
            a = arb(str(half_width))
            smooth_maps = {}
            smooth_cache = {}
            for target in range(13):
                for source in range(13):
                    lower = min(target, source)
                    upper = max(target, source)
                    between = labels[lower + 1 : upper]
                    key = (
                        labels[target],
                        labels[source],
                        tuple(
                            between.count(label)
                            for label in ("edge", "bridge", "center")
                        ),
                        degrees[source],
                        target == source,
                    )
                    if key not in smooth_cache:
                        gap = sum(
                            pilot_lengths[lower + 1 : upper], arb(0)
                        )
                        smooth_metadata = _smooth_map_cache_metadata(
                            half_width=half_width,
                            target_label=labels[target],
                            source_label=labels[source],
                            gap_signature=key[2],
                            source_degree_count=degrees[source],
                            smooth_degree=smooth_degree,
                            maximum_smooth_power=maximum_smooth_power,
                            precision=max(precision, 128),
                            same_block=target == source,
                        )
                        smooth_cache_path = None
                        block = None
                        if cross_map_cache_dir is not None:
                            smooth_cache_path = _matrix_cache_path(
                                cross_map_cache_dir,
                                smooth_metadata,
                                "smooth-map",
                            )
                            block = _load_arb_matrix(
                                smooth_cache_path,
                                smooth_metadata,
                                arb,
                                arb_mat,
                            )
                        if block is None:
                            block = arb_mat(smooth_degree, degrees[source])
                            for power, coefficient in enumerate(coefficients):
                                power_matrix = _power_block_rectangular(
                                    arb,
                                    arb_mat,
                                    pilot_lengths[target],
                                    pilot_lengths[source],
                                    gap,
                                    smooth_degree,
                                    degrees[source],
                                    power,
                                    target == source,
                                )
                                rational = (
                                    arb(coefficient.numerator)
                                    / coefficient.denominator
                                )
                                block += (
                                    -a * rational * a**power
                                ) * power_matrix
                            if smooth_cache_path is not None:
                                _save_arb_matrix(
                                    smooth_cache_path,
                                    block,
                                    smooth_metadata,
                                )
                        smooth_cache[key] = block
                    smooth_maps[target, source] = smooth_cache[key]

        ctx.prec = working_precision
        _, _, lengths = _arb_breakpoints_lengths(arb, half_width)
        offsets = _offsets(degrees)
        total = offsets[-1]
        full_bands = [
            arb_mat(total, total) for _ in range(len(boundaries) - 1)
        ]
        cross_maps = {}
        q_cache = {}
        for target in range(13):
            for source in range(13):
                if source == target:
                    continue
                lower = min(target, source)
                upper = max(target, source)
                between = labels[lower + 1 : upper]
                gap_signature = tuple(
                    between.count(label)
                    for label in ("edge", "bridge", "center")
                )
                geometry = (
                    labels[target],
                    labels[source],
                    gap_signature,
                    degrees[source],
                )
                if geometry not in cross_maps:
                    gap = sum(lengths[lower + 1 : upper], arb(0))
                    builder = (
                        _build_adjacent_full_matrix
                        if abs(target - source) == 1
                        else _build_separated_full_matrix
                    )
                    arguments = (
                        arb,
                        arb_mat,
                        acb,
                        lengths[target],
                        lengths[source],
                    )
                    if builder is _build_separated_full_matrix:
                        arguments += (gap,)
                    metadata = _cross_map_cache_metadata(
                        half_width=half_width,
                        target_label=labels[target],
                        source_label=labels[source],
                        gap_signature=gap_signature,
                        source_degree_count=degrees[source],
                        first_degree=first_degree,
                        last_degree=last_degree,
                        working_precision=working_precision,
                        builder_kind=(
                            "adjacent"
                            if builder is _build_adjacent_full_matrix
                            else "separated"
                        ),
                    )
                    cached = None
                    cache_path = None
                    if cross_map_cache_dir is not None:
                        cache_path = _matrix_cache_path(
                            cross_map_cache_dir, metadata, "cross-map"
                        )
                        cached = _load_arb_matrix(
                            cache_path, metadata, arb, arb_mat
                        )
                    if cached is None:
                        cached = builder(
                            *arguments,
                            degrees[source],
                            first_degree,
                            last_degree,
                            q_cache,
                        )
                        if cache_path is not None:
                            _save_arb_matrix(cache_path, cached, metadata)
                    cross_maps[geometry] = cached
                cross_maps[target, source] = cross_maps[geometry]

        for target in range(13):
            local_bands = [
                arb_mat(total, total) for _ in range(len(boundaries) - 1)
            ]
            band_index = 0
            for row, degree in enumerate(range(first_degree, last_degree)):
                while degree >= boundaries[band_index + 1]:
                    band_index += 1
                vector = arb_mat(1, total)
                for source in range(13):
                    for source_degree in range(degrees[source]):
                        if source == target:
                            value = (
                                arb(
                                    (2 * degree + 1)
                                    * (2 * source_degree + 1)
                                ).sqrt()
                                / (
                                    (degree - source_degree)
                                    * (degree + source_degree + 1)
                                )
                                if (degree + source_degree) % 2 == 0
                                else arb(0)
                            )
                        else:
                            value = cross_maps[target, source][row, source_degree]
                            if source < target and (degree + source_degree) % 2:
                                value = -value
                        if smooth_maps is not None and degree < smooth_degree:
                            value += smooth_maps[target, source][
                                degree, source_degree
                            ]
                        vector[0, offsets[source] + source_degree] = value
                local_bands[band_index] += vector.transpose() * vector
            for band, local in zip(full_bands, local_bands):
                band += local

        even_transform, odd_transform = _parity_transforms(
            arb, arb_mat, degrees, offsets
        )
        results = []
        for (band_first, band_last), full in zip(
            zip(boundaries[:-1], boundaries[1:]), full_bands
        ):
            even = even_transform.transpose() * full * even_transform
            odd = odd_transform.transpose() * full * odd_transform
            even_midpoint, even_radius = _export(even)
            odd_midpoint, odd_radius = _export(odd)
            results.append(
                ArbThirdWindowNearTailGram(
                    even_midpoint=even_midpoint,
                    even_radius=even_radius,
                    odd_midpoint=odd_midpoint,
                    odd_radius=odd_radius,
                    interval_degrees=degrees,
                    first_degree=band_first,
                    last_degree=band_last,
                    precision=precision,
                    working_precision=working_precision,
                    maximum_smooth_power=maximum_smooth_power,
                )
            )
    finally:
        ctx.prec = previous_precision

    return results[0] if band_boundaries is None else tuple(results)
