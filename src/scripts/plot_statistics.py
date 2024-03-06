from utils import ONE_COL_GOLDEN_RATIO_HEIGHT_INCH, ONE_COL_WIDTH_INCH
import matplotlib.pyplot as plt
from paths import output, figures, scripts

plt.style.use(scripts / "lamalab.mplstyle")
import pandas as pd


import numpy as np
from plotutils import range_frame


def question_count_barplot(df):
    fig, ax = plt.subplots(
        1,
        2,
        figsize=(ONE_COL_WIDTH_INCH, ONE_COL_GOLDEN_RATIO_HEIGHT_INCH),
        sharex=True,
    )

    df_mcq = df[df["is_classification"]]
    df_not_mcq = df[~df["is_classification"]]

    topics_mcq, counts_mcq = (
        df_mcq["topic"].value_counts().index,
        df_mcq["topic"].value_counts().values,
    )
    topics_general, counts_general = (
        df_not_mcq["topic"].value_counts().index,
        df_not_mcq["topic"].value_counts().values,
    )
    # ensure general topics are in the same order as mcq topics. Sort keys and values accordingly
    topics_general, counts_general = zip(
        *sorted(
            zip(topics_general, counts_general), key=lambda x: topics_mcq.get_loc(x[0])
        )
    )

    all_counts = np.concatenate([counts_mcq, counts_general])

    ax[0].hlines(topics_mcq, xmin=0, xmax=topics_mcq, linewidth=5, alpha=0.2)
    ax[0].plot(counts_mcq, topics_mcq, "o", markersize=5, alpha=0.6)
    ax[0].set_xscale("log")
    range_frame(ax[0], all_counts, np.arange(len(topics_general)))

    ax[1].hlines(topics_general, xmin=0, xmax=topics_general, linewidth=5, alpha=0.2)
    ax[1].plot(counts_general, topics_general, "o", markersize=5, alpha=0.6)
    ax[1].set_xscale("log")
    range_frame(ax[1], all_counts, np.arange(len(topics_general)))

    ax[0].set_xlabel("Number of Questions")

    fig.savefig(figures / "question_count_barplot.pdf", bbox_inches="tight")


def plot_question_statistics():
    df = pd.read_pickle(output / "questions.pkl")
    question_count_barplot(df)


if __name__ == "__main__":
    plot_question_statistics()
