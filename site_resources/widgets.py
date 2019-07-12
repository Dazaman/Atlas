import ipywidgets as widgets
from IPython.display import display

w = widgets.Dropdown(
    options=[(' '),('Underworld','Underworld'),('Badlands', 'Badlands'),('Coupled', 'Coupled'),('PyGplates', 'PyGplates'),('Gplates & Citcoms', 'Gplates & Citcoms'),('Uncategorised', 'Uncategorised')],
    value= ' ',
    description='Category:',
    disabled=False,
)

badlands = widgets.Checkbox(
    value=False,
    description='badlands',
    disabled=False,
)

underworld = widgets.Checkbox(
    value=False,
    description='underworld',
    disabled=False,
)

pygplates = widgets.Checkbox(
	value=False,
    description='pygplates',
    disabled=False,
    # visibility='hidden',
)
gplates = widgets.Checkbox(
    value=False,
    description='gplates',
    disabled=False,
)
citcoms = widgets.Checkbox(
    value=False,
    description='citcoms',
    disabled=False,
)
gmt = widgets.Checkbox(
    value=False,
    description='gmt',
    disabled=False,
)
def on_change(change):
    if change['type'] == 'change' and change['name'] == 'value':
        print "changed to %s" % change['new']

w.observe(on_change)
badlands.observe(on_change)
underworld.observe(on_change)
pygplates.observe(on_change)
gplates.observe(on_change)
citcoms.observe(on_change)
gmt.observe(on_change)

# underworld.layout.visibility = 'none'
display(w)
display(badlands)
display(underworld)
display(pygplates)

# For config.yml description
  # <br><br>The Atlas is a top-level visual summary of end-member numerical models that the BGH is created.
  # <br><br>
  # <p><a href="https://github.com/rsbyrne/demonstration"><h2><b>Contribute to the Atlas</b></h2></a></p>
  # <p>1. Clone the repository</p>
  # <p>2. Go to the "pages" directory and make a copy of the "example" folder</p>
  # <p>3. Open up the Jupyter notebook and follow the instructions (make sure to run the code at the bottom when you are finished!)</p>
  # <p>4. Push your changes back up to the repository.</p>