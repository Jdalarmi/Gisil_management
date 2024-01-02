import base64
from io import BytesIO
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt


def generate_bar(categories, values):
    fig, ax = plt.subplots()
    bar_labels = ['red', 'blue']
    bar_colors = ['tab:red', 'tab:blue']

    bars = ax.bar(categories, values, label=bar_labels, color=bar_colors)

    ax.set_title('Gestão de gasto com materiais')
    for bar, value in zip(bars, values):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, height, f'{value}', 
                    ha='center', va='bottom')

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return f'data:image/png;base64,{image_base64}'

