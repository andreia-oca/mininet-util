'''
Plot queue occupancy over time
'''
from helper import *
import plot_defaults

plot_defaults.quarter_size()

from matplotlib.ticker import MaxNLocator
from pylab import figure


parser = argparse.ArgumentParser()
parser.add_argument('--files', '-f',
                    help="Queue timeseries output to one plot",
                    required=True,
                    action="store",
                    nargs='+',
                    dest="files")

parser.add_argument('--maxy',
                    help="Max mbps on y-axis..",
            type=int,
                    default=200,
                    action="store",
                    dest="maxy")

parser.add_argument('--miny',
                    help="Min mbps on y-axis..",
                    type=int,
                    default=0,
                    action="store",
                    dest="miny")

parser.add_argument('--legend', '-l',
                    help="Legend to use if there are multiple plots.  File names used as default.",
                    action="store",
                    nargs="+",
                    default=None,
                    dest="legend")

parser.add_argument('--out', '-o',
                    help="Output png file for the plot.",
                    default=None, # Will show the plot
                    dest="out")

parser.add_argument('--cdf',
                    help="Plot CDF of queue timeseries (first 10 and last 10 values are ignored)",
                    default=False,
                    dest="cdf",
                    action="store_true")

parser.add_argument('--labels',
                    help="Labels for x-axis if summarising; defaults to file names",
                    required=False,
                    default=[],
                    nargs="+",
                    dest="labels")

parser.add_argument('--every',
                    help="If the plot has a lot of data points, plot one every EVERY (x,y) point (default 1).",
                    default=1,
                    type=int)

args = parser.parse_args()
if args.labels is None:
    args.labels = args.files

if args.legend is None:
    args.legend = []
    for file in args.files:
        args.legend.append(file)

to_plot=[]
def get_style(i):
    if i == 0:
        return {'color': 'red'}
    if i == 1:
        return {'color': 'black', 'ls': '-.'}
    else:
        return {'color': 'orange'}

print args.files
fig = figure()
ax = fig.add_subplot(111)
for i, f in enumerate(args.files):
    data = read_list(f)
    xaxis = map(float, col(0, data))
    start_time = xaxis[0]
    xaxis = map(lambda x: x - start_time, xaxis)
    qlens = map(float, col(1, data))

    if args.cdf:
        to_plot.append(qlens[10:-10])
    else:
        xaxis = xaxis[::args.every]
        qlens = qlens[::args.every]
        ax.plot(xaxis, qlens, label=args.legend[i], lw=2, **get_style(i))

    ax.xaxis.set_major_locator(MaxNLocator(4))


plt.title("Queue Occupancy", fontsize=24)
plt.ylabel("Queue size", fontsize=16)
plt.grid(True)
plt.ylim((args.miny,args.maxy))

if args.cdf:
    fig = figure()
    ax = fig.add_subplot(111)
    for i,data in enumerate(to_plot):
        xs, ys = cdf(map(int, data))
        ax.plot(xs, ys, label=args.legend[i], lw=2, **get_style(i))
        # plt.ylabel("Fraction")
        plt.xlabel("Packets", fontsize=16)
        plt.ylim((0, 1.0))
        plt.legend(args.legend, bbox_to_anchor=(1.05, 1))
        # plt.legend(args.legend, loc="upper left")
        plt.title("Queue Occupancy CDF", fontsize=24)
        ax.xaxis.set_major_locator(MaxNLocator(4))
else:
    plt.xlabel("Seconds", fontsize=16)
    if args.legend:
        plt.legend(args.legend, bbox_to_anchor=(1.05, 1))
        # plt.legend(args.legend, loc="upper left")
    else:
        plt.legend(args.files)

if args.out:
    plt.savefig(args.out, bbox_inches="tight")
else:
    plt.show()
