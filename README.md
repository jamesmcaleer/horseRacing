# Horse Racing 🐎
A digital horse racing simulator to continue my grandfather's holiday tradition

## Odds Simulation

The **ChanceHandler** creates a set of 8 odds (ex: 2:1, 9:1)

8 random speed graphs are generated and sorted

Based on the odds, each horse has a certain percent chance to be given the fastest available speed graph

This way, even a horse with the lowest odds has a chance to win the race

When a horse is picked, the speed graph becomes _unavailable_, the process repeats using the _next_ fastest speed graph and picks another horse

Once this process is complete, the program has 8 _horse skeletons_ but there are no graphics, numbers, or colors attached

##


