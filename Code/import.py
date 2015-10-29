import pandas as pd
import numpy as np
import re
from datetime import datetime
from dateutil import tz
import pandas as pd
from datetime import datetime
from dateutil import tz
import re
import nltk
import sys
from gensim import corpora, models, similarities
import gensim.parsing.preprocessing as preprocess
import gensim.matutils as mat
from nltk.stem import *

from nltk.stem.porter import *
from nltk.stem.snowball import SnowballStemmer

import pandas as pd
import numpy as np
from gensim import corpora, models, similarities
import gensim.parsing.preprocessing as preprocess
import gensim.matutils as mat
import pyLDAvis.gensim
import sys  

import seaborn as sns

import matplotlib.pyplot as plt
from matplotlib import style
#%matplotlib inline
style.use('ggplot')
import graphlab

reload(sys) 

from pydoc import help
from scipy.stats.stats import pearsonr

from numpy import corrcoef, sum, log, arange
from numpy.random import rand
from pylab import pcolor, show, colorbar, xticks, yticks