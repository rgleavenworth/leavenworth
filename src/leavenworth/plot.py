import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
import os
from os.path import expanduser
from matplotlib import ticker
import matplotlib.ticker as mtick
import matplotlib.lines as mlines
import numpy as np

lc_colors = ["#7C9eA6", "#2e4959",'#cc9933', '#cccccc', '#434343']

def lc_fonts(font_dir = None):
    """Use Leavenworth fonts"""
    if font_dir:
        pass
    else:
        font_dir = os.path.join(expanduser('~'), 'lcfonts')
    for font in font_manager.findSystemFonts(font_dir):
        font_manager.fontManager.addfont(font)
    return None

def set_params(plot_style, plot_type = 'glassnode', font_scale = 1.5, linewidth = 2.5, title_color = '#cc9933', font = 'Legacy Sans ITC Pro', image_scale = 1, size = 8, aspect = 2,  **kws):
    """Function stylizes plot paramaters according to Leavenworth theme defaults."""

    from seaborn import set_context
    sns.set(font=font)
    set_context("notebook", font_scale = font_scale, rc = {"lines.linewidth":linewidth})

    if plot_style == 'dark':
        lc_fonts(**kws)
        from jupyterthemes import jtplot
        jtplot.style(theme='onedork')
        set_context("notebook", font_scale = font_scale, rc = {"lines.linewidth":linewidth})
        title_color = title_color
        title_font = font
        font = font
        image_scale = image_scale
    else:
        lc_fonts(**kws)
        plt.style.use('fivethirtyeight')
        set_context("notebook", font_scale = font_scale, rc = {"lines.linewidth":linewidth})
        title_color = title_color
        font = font
        title_font = font
        image_scale = image_scale
    
    params = {}
    params['title_color'] = title_color
    params['font'] = font
    params['title_font'] = font
    params['image_scale'] = image_scale
    params['size'] = size
    params['aspect'] = aspect
    
    # Create an array with the colors you want to use
    if plot_type == 'glassnode':
        colors = ['#000000', '#cc9933', "#2e4959", "#7C9eA6", '#cccccc', '#434343']
    elif plot_type == 'performance':
        colors = ['#cc9933', "#2e4959", '#cccccc', "#7C9eA6", '#434343', '#000000']
    else:
        raise Exception('Unknown plot type')
    # Set your custom color palette
    sns.set_palette(sns.color_palette(colors))
    return(params)

def whiten_grid(f, ax):
    """Override exiting facecolors on plots and whiten plot area"""
    f.patch.set_facecolor((1,1,1))
    ax.set_facecolor((1,1,1))
    return None 

def stylize_spines(ax, color = '#2e4959', lw = 4):
    """Function stylizes spines according to Leavenworth theme defaults. Defaults can be overridden with color and lw switches"""
    ax.spines['top'].set_color(color)
    ax.spines['top'].set_linewidth(lw)
    ax.spines.top.get_bounds()
    return None

def glassnode_plot(data, plot_style = 'leavenworth', price = None, ylabel = None, yaxis = 'linear', rolling = None, linecolor = '#cc9933', percent = False, price_percent = False, dual_plot = True, price_axis = 'log', price_alpha = 1, currency = 'BTC', size = 8, aspect = 2, image_scale = 1, whiten = True, grid = True, price_grid = False, price_lw = 1.5, price_lc = lc_colors[0], start_date = None, price_plot = False, price_label = None, log_formatter = True, title = None, style = 'line', title_loc = 'left', title_fs = 24, stylize = True, lw = 4):
    """Basic setup for Glassnode data plots"""
    if plot_style == 'leavenworth':
        params = set_params('leavenworth', plot_type = 'glassnode')
    elif plot_style == 'mailchimp':
        params = set_params('leavenworth', plot_type = 'glassnode', font_scale = 1, image_scale = 1, size = 4, linewidth = 1.5)
        size = 4
        title_fs = 16
        lw = 2
    else:
        params = set_params('dark')
    if dual_plot and isinstance(price, type(None)):
        raise Exception('No price data given, this can not be a dual plot')
    if isinstance(start_date, str):
        data = data.loc[start_date:]
        if dual_plot:
            price = price.loc[start_date:]
    f, ax = plt.subplots(figsize = (aspect*image_scale*size,image_scale*size))
    if rolling:
        data = data.rolling(rolling).mean()
        if percent:
            data = data*100
    else:
        pass
    if style == 'line':
        ax = sns.lineplot(data = data, color = linecolor)
    elif style == 'bar':        
        ax = sns.barplot(data = data.reset_index(), x = 't', y = data.name)
    else:
        raise Exception('Invalid style. Supported types are line and bar')
    if yaxis == 'log':
        ax.set_yscale('log')
        if log_formatter:
            ax.yaxis.set_major_formatter(ticker.FormatStrFormatter("%d"))
    if percent:
        ax.yaxis.set_major_formatter(mtick.PercentFormatter())
    if price_plot:
        if price_axis == 'log':
            plt.yscale('log')
        if log_formatter:
            ax.yaxis.set_major_formatter(ticker.FormatStrFormatter("%d"))
    plt.xlabel('')
    plt.ylabel(ylabel)
    ax.grid(grid)
    ax.grid(grid)
    if dual_plot:
        ax1 = ax.twinx()
        ax1 = sns.lineplot(data = price, color = price_lc, linewidth = price_lw, alpha = price_alpha)
        if price_percent:
            ax1.yaxis.set_major_formatter(mtick.PercentFormatter())
        if price_axis == 'log':
            ax1.set_yscale('log')
            if log_formatter:
                ax1.yaxis.set_major_formatter(ticker.FormatStrFormatter("%d"))
        if price_label:
            plt.ylabel(price_label)
        else:
            plt.ylabel('%s-USD'%currency)
        ax1.grid(price_grid)
    if whiten:
        whiten_grid(f, ax)
    if stylize:
        if dual_plot:
            stylize_spines(ax1, lw = lw)
        else:
            stylize_spines(ax, lw = lw)
    if title:
        plt.title(title, fontname = params['title_font'], loc = title_loc, y = 1.02, fontsize = title_fs)
    if dual_plot:
        return(f, ax, ax1)
    else:
        return(f, ax)

def add_legend(labels, colors = ['#cc9933','#7C9eA6'], legend_marker = '_'):
    """Function sets up legend defaults"""
    if type(colors) != type(labels):
        raise Exception('colors and labels need to be the same data type. Supported data types are str and list')
    if isinstance(colors, str):
        colors = [colors]
        labels = [labels]
    handles = list()
    for c, l in zip(colors, labels):
        p = mlines.Line2D([], [], color=c, marker=legend_marker, label=l)
        handles.append(p)
    return handles

# def yahoo_plot():    
#     return(f, ax)

def fng_plot(df, plot_style = 'leavenworth', size = 8, aspect = 2, image_scale = 1, stylize = True, whiten = True, title = 'Fear and greed index'.upper(), title_loc = 'left', title_fs = 24, linecolor = '#cc9933',):
    if plot_style == 'leavenworth':
        params = set_params('leavenworth', plot_type = 'glassnode')
    else:
        params = set_params('dark')
    f, ax = plt.subplots(figsize = (aspect*image_scale*size,image_scale*size))
    ax = sns.lineplot(data = df, y = 'VALUE', x = 'TIMESTAMP', color = linecolor)
    if whiten:
        whiten_grid(f, ax)
    if stylize:
        stylize_spines(ax)
    plt.title(title, fontname = params['title_font'], loc = title_loc, y = 1.02, fontsize = title_fs)
    return f, ax

def change_width(ax, new_value) :
    for patch in ax.patches :
        current_width = patch.get_width()
        # we change the bar width
        patch.set_width(new_value)
    return ax

def performance_plot(data, plot_style = 'leavenworth', x = 'YTD', size = 4, aspect = 2.5, image_scale = 2, whiten = True, stylize = True, title = None, title_loc = 'left', title_fs = 24, shrink_bars = True, shrink_factor = 0.12):
    """Basic setup for performance plots"""
    if plot_style == 'leavenworth':
        params = set_params('leavenworth', plot_type = 'performance')
    else:
        params = set_params('dark')
    
    f, ax = plt.subplots(figsize = (aspect*image_scale*size,image_scale*size))
    ax = sns.barplot(data = data, x = x, y = 'RETURN', hue = 'TICKER')
    ax.yaxis.set_major_formatter(mtick.PercentFormatter())
    if 'MONTH' in data.columns.tolist():
        ax.set_xticks(np.arange(0.5, len(data.MONTH.unique()), 1))
        ax.set_xticklabels(ax.xaxis.get_majorticklabels())
        ax.grid(True)
    if 'YTD' in data.columns.tolist():
        ax.set(xticklabels=[])
        plt.xlabel('')
    if 'INCEPTION' in data.columns.tolist():
        ax.set(xticklabels=[])
        plt.xlabel('')        
    plt.legend(bbox_to_anchor = (1,1))
    plt.xticks(rotation = 0)
    if shrink_bars:
        change_width(ax, shrink_factor)
    if whiten:
        whiten_grid(f, ax)
    if stylize:
        stylize_spines(ax)
    if title:
        plt.title(title, fontname = params['title_font'], loc = title_loc, y = 1.02, fontsize = title_fs)
    if 'YTD' in data.columns.tolist() or 'INCEPTION' in data.columns.tolist():  
        bars = list(range(0,len(ax.containers)))
        for bar in bars:
            ax.bar_label(ax.containers[bar],  fmt='%.2f')
    return (f, ax)