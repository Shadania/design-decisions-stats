import shutil

characs = [
    "comment avg size",
    "comment count",
    "description size",
    "duration",
    "num_attachments",
    "votes",
    "watches",
]

import os
os.makedirs('forlatex/rq3/', exist_ok=True)
os.makedirs('forlatex/rq2/', exist_ok=True)

for charac in characs:
    files = [
        f"{charac}_simple_plot_arrows",
        f"{charac}_simple_inverted_plot_arrows",
        f"{charac}_plot_arrows",
        f"{charac}_inverted_plot_arrows"
    ]
    for file in files:
        shutil.copy(f"rq3_{charac}/{file}.png", f"forlatex/rq3/{file}.png")
    file = f"{charac}_plot_arrows.png"
    shutil.copy(f"rq2_{charac}/{file}", f"forlatex/rq2/{file}")