from os import path
from collections import Counter
from wordcloud import WordCloud
from scipy.misc import imread
import matplotlib.pyplot as plt
import numpy as np


class Plots:
    """
    A simple plot library for token or tag lists. Available methods:
        - word_cloud: plot a word cloud of input tokens/tags, each represented with dimensions proportional
        to their frequencies;
        - word_histogram: plot a bar histogram of tokens/tags frequencies.
    Input:
        - words (mandatory): a list (or Counter) of strings, representing tokens/tags to be plotted.
    """

    def __init__(self, words):
        if not isinstance(words, Counter):
            self.words = Counter(words)
        else:
            self.words = words

    def word_cloud(self, image_name):
        """
        Plot a word cloud of input tokens/tags, each represented with dimensions proportional
        to their frequencies, and save the image to disk.
        Input:
            - image_name (mandatory): a string representing the desired name for the output image
        """

        d = path.dirname(__file__)
        mask = imread(path.join(d, "mask.png"))
        wc = WordCloud(background_color="black", mask=mask).generate_from_frequencies(self.words)
        image = wc.to_image()
        image.show(title=image_name + ".png")
        image.save(path.join("images", image_name + ".png"))

    def word_histogram(self, image_name, n_mostfreq=10):
        """
        Plot a bar histogram of tokens/tags frequencies, and save the image to disk.
        Input:
            - image_name (mandatory): a string representing the desired name for the output image;
            - n_mostfreq (optional, default=10): an integer representing the number of most frequent tokens/tags
            to be represented.
        """

        labels, values = zip(*self.words.most_common(n_mostfreq))

        # sort your values in descending order
        indSort = np.argsort(values)[::-1]

        # rearrange your data
        labels = np.array(labels)[indSort]
        values = np.array(values)[indSort]

        indexes = np.arange(len(labels))

        width = 0.8
        plt.figure(0).canvas.set_window_title(image_name)
        plt.title(image_name)
        plt.barh(indexes, values, width)

        # add labels
        plt.yticks(indexes + width * 0.5/n_mostfreq, labels)
        plt.show()
        plt.savefig(path.join("images", image_name + ".png"), dpi=100)
