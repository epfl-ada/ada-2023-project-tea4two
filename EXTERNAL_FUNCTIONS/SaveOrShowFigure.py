OUTPUT_FOLDER_HTML = './IMAGES/html/'
OUTPUT_FOLDER_WEBSITE_HTML = '../jeanlefort.github.io/img/html/'
def export_plots(fig, name):
    fig.write_html(OUTPUT_FOLDER_HTML + name + ".html")
    fig.write_html(OUTPUT_FOLDER_WEBSITE_HTML + name + ".html")

    return fig.show()