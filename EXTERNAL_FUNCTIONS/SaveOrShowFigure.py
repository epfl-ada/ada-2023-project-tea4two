from kaleido.scopes.plotly import PlotlyScope
from IPython.display import Markdown

# GLOBAL VARIABLE: display_option = "static" or "dynamic"
DISPLAY_OPTION = "static" #for github mainly
#DISPLAY_OPTION = "dynamic" #for interactive display

def save_or_show_figure(fig, filename, format="svg", display_option=DISPLAY_OPTION):
    scope = PlotlyScope(
        plotlyjs="https://cdn.plot.ly/plotly-latest.min.js",
    )

    if format == "svg":
        with open(filename, "wb") as f:
            f.write(scope.transform(fig, format="svg"))
    else:
        fig.write_image(filename)

    if display_option == "static":
        return Markdown("""![{filename}]({filename})""".format(filename=filename))
    else:
        return fig.show()