OUTPUT_FOLDER_HTML = './IMAGES/html/'
OUTPUT_FOLDER_WEBSITE_HTML = '../GuillaumeSalha.github.io/img/html/'
OUTPUT_FOLDER_PNG = './IMAGES/png/'
OUTPUT_FOLDER_WEBSITE_PNG = '../GuillaumeSalha.github.io/img/png/'

def export_plots(fig, name):
    fig.write_html(OUTPUT_FOLDER_HTML + name + ".html")
    fig.write_html(OUTPUT_FOLDER_WEBSITE_HTML + name + ".html")
    #fig.write_image(OUTPUT_FOLDER_PNG + name + ".png")
    #fig.write_image(OUTPUT_FOLDER_WEBSITE_PNG + name + ".png")

    # return Image(output_img_folder + name + ".png")
    #return fig.show()