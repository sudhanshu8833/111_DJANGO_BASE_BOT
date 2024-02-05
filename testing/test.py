import pandas as pd

from finta import TA
# Create a DataFrame so 'ta' can be used.
df = pd.DataFrame()

# Help about this, 'ta', extension
# help(df.ta)

# List of all indicators
print(df.ta.indicators())
df.ta

# Help about an indicator such as bbands
# help(ta.bbands)