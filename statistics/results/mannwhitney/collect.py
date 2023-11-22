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

for charac in characs:
    files = [
        f"{charac}_simple_plot_arrows",
        f"{charac}_simple_inverted_plot_arrows",
        f"{charac}_plot_arrows",
        f"{charac}_inverted_plot_arrows"
    ]
    for file in files:
        shutil.copy(f"rq3_{charac}/{file}.png", f"forlatex/{file}.png")