
"""Plotly layout for bounded categorical FLEX D7 charts.

This is presentation only: source categories and counts remain unchanged.
"""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from src.explorer_charts import sample_category_counts
from src.i18n import LANGUAGES, display_code, tr


_OUTCOME_LABEL_KEYS = {
    "Completion": "chart_end_completion",
    "Disruption": "chart_end_disruption",
    "Extinction": "chart_end_extinction",
}

_CHART_FIELDS = {
    "fuel_raw": "fuel",
    "test_end_raw": "chart_end_title",
    "qc_dap_d4_record_status": "chart_qc_title",
}


def make_count_chart(
    records: pd.DataFrame,
    field: str,
    language: str,
) -> go.Figure:
    """Return a readable categorical count chart, without altering records.

    Outcomes are horizontal for long translated labels. Fuel and D4 QC
    display the original category codes and offer translations on hover.
    All numerical count axes start at zero and cannot be zoomed or panned.
    """
    if language not in LANGUAGES:
        raise ValueError(f"Unsupported interface language: {language}")
    if field not in _CHART_FIELDS:
        raise ValueError(f"Unsupported count chart field: {field}")

    counts = sample_category_counts(records, field).copy(deep=True)
    counts["raw_category"] = counts["category"].map(str)
    counts["hover_category"] = counts["raw_category"].map(
        lambda raw: display_code(raw, language)
    )

    title = tr(_CHART_FIELDS[field], language)
    count_label = tr("audited_records", language)

    count_max = (
        int(counts["sample_records"].max())
        if not counts.empty else 0
    )
    axis_limit = max(2, count_max + 2)

    if field == "test_end_raw":
        counts["plot_category"] = counts["raw_category"].map(
            lambda raw: (
                tr(_OUTCOME_LABEL_KEYS[raw], language)
                if raw in _OUTCOME_LABEL_KEYS else raw
            )
        )

        figure = px.bar(
            counts,
            x="sample_records",
            y="plot_category",
            orientation="h",
            text="sample_records",
            title=title,
            custom_data=["hover_category"],
            labels={
                "sample_records": count_label,
                "plot_category": title,
            },
        )

        figure.update_xaxes(
            range=[0, axis_limit],
            dtick=1,
            fixedrange=True,
            title=None,
        )

        figure.update_yaxes(
            categoryorder="array",
            categoryarray=counts["plot_category"].tolist(),
            fixedrange=True,
            title=None,
        )

        figure.update_traces(
            hovertemplate=(
                "<b>%{customdata[0]}</b><br>"
                + count_label + ": %{x}<extra></extra>"
            )
        )

        left_margin = 153 if language == "ru" else 100

    else:
        # Keep QC codes such as REVIEW/VERIFIED visible.
        counts["plot_category"] = counts["raw_category"]

        figure = px.bar(
            counts,
            x="plot_category",
            y="sample_records",
            text="sample_records",
            title=title,
            custom_data=["hover_category"],
            labels={
                "sample_records": count_label,
                "plot_category": title,
            },
        )

        figure.update_yaxes(
            range=[0, axis_limit],
            dtick=1,
            fixedrange=True,
            title=None,
        )

        figure.update_xaxes(
            fixedrange=True,
            title=None,
        )

        figure.update_traces(
            hovertemplate=(
                "<b>%{customdata[0]}</b><br>"
                + count_label + ": %{y}<extra></extra>"
            )
        )

        left_margin = 40

    figure.update_traces(
        textposition="outside",
        cliponaxis=False,
    )

    figure.update_layout(
        height=355,
        showlegend=False,
        margin=dict(
            l=left_margin,
            r=20,
            t=55,
            b=38,
        ),
        title=dict(x=0.02, xanchor="left"),
    )

    return figure
