# MK8D-analysis

At the time of updating this readme, I have been playing the new Mario Kart on the Nintendo Switch for more than two years.
The peculiarity of this game, a new feature introduced in this iteration, is the high level of customization of the karts and the bikes.
Before playing a Grand Prix, either locally or online, the player must choose:

- A **character**
- A **bike** or a **kart**
- The **tyres**
- The **glider**

each of them with 6 visible stats *(ground speed, acceleration, weight, handling, traction, mini turbo)* and 6 more hidden stats *(air speed, antigravity speed, water speed, water handling, air handling, antigravity handling)*.

The question that soon arose was: how can I choose a build (character, kart, tyres, glider) that is the best?
*It is possible to finally defeat the superior Japanese players in the 200cc category?*

## The data

All the data has been gathered from the [Mario Kart 8 Deluxe Wiki](https://www.mariowiki.com/Mario_Kart_8_Deluxe_in-game_statistics).

I soon found that not each entity is unique;
up to 4 karts, characters, tyres and gliders can share the same stats.
For example, the characters *Waluigi*, *Donkey Kong* and *Roy Koopa* all share the same stats; the same goes for the karts *Streetle* and the *Landship*.
To reduce the size of the database *(and somehow make the data more manageable)*, I grouped the entities that share the same stats, by giving them a shared id.
One more table, linking the entity id to their relative names, was needed.

### Cleaning the data

The data (found as `.csv` files in the `data/dirty` folder) cannot be handled as-is by the program.

So this is where the `clean_files.py` comes in. It:

1. Loads all the files in the `data/dirty` folder
2. Cleans the rows, removing redundant lines and superfluous details
3. Merges the duplicated rows, by assigning them the same id
4. Saves the output data in both `csv` and `sqlite` format

This is where the `MK8D` sqlite database is created.

I chose to use `sqlite` because it allows one to easily query the data via `SQL`; while not being a language that I particularly like, I figured out that it would have made my life easier in this case.
The other option was to use a no-SQL database, like `MongoDB`, but I figured that making queries would be more difficult.

## The analysis

This is where things got complicated.

All the data was in a database; now I needed to extract it.

Only recently I found out the power of Python dunder ~~mifflin~~ methods, and I decided to use them.
*Operators overriding? Count me in!*

I quickly discarded `dataclasses`, as they are not meant to be used as containers for data, but rather as a way to represent data; due to my love of reinventing the wheel, I created a new `Entity` class, better suited for my needs.

### Create builds

The script `create_builds.py` loads all the entities from the database via the `MK8Deluxe` class, a wrapper around the `sqlite3` module.
Via the aforementioned dunder methods, the single entities loaded are then added together, creating an instance of the `Build` class.

The builds are then saved into another `sqlite` database and inside a (pretty big) `csv` file to be used later.

### Find builds

The script `find_builds.py` loads all the created builds in the previous step and filters them according to the user's needs, thanks to the `MK8DeluxeBuilds` class.
To do so, the script:

- Accepts a minimum and maximum value for each stat
- Computes a score for each build, according to some custom weights
- Sorts the builds in an order according to the user's needs
- Limits the number of builds to be shown

The part relative to the sorting is implemented via an algorithm called `top-k`.
All the entities manipulations are done via dunder methods, which makes the code very readable *(I hope)* as it reduces the overall verbosity and makes the code more compact.

The output of the script can be either printed to the console "raw" *(in a human-readable format)*, `json`, `csv`, table formatted in `markdown`, or `toml` format.

## The results

Now the hard part is setting custom weights and filters.
How is it possible to balance the stats in order to get the best build?

Long before making this program, I read a lot of online articles and watched a lot of videos discussing the best builds.
Some would prefer acceleration over velocity, others would prefer handling over traction.

After playing for a long while, I found out that:

- Miniturbo is a really important stat, as I get a lot of them due to my continuous drifting
- Acceleration is more important than speed, as online lobbies make aggressive use of items
- Handling and traction are pretty important, but not as much as the other stats
- The best build is the one that has balanced stats

So I tweaked the weights and the filters, finally setting:

- The **minimum ground speed** to 12
- The **minimum ground acceleration** to 12
- The **minimum miniturbo** to 5
- **Ground speed** weight to 0.5
- **Acceleration** weight to 0.5
- **Miniturbo** weight to 0.1

The top 5 builds, sorted by *score* and the *standard deviation* of the stats, are the following:

|score|score_dev|id|ground_speed|water_speed|air_speed|antigravity_speed|acceleration|weight|ground_handling|water_handling|air_handling|antigravity_handling|miniturbo|on_road_traction|off_road_traction|invincibility|driver|vehicle|tyre|glider |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 14.4 | 2.986636904613616 | 9137 | 12 | 17 | 15 | 12 | 14 | 11 | 10 | 8 | 8 | 9 | 14 | 10 | 9 | 9 | Bowser, Morton | Pipe Frame | Roller, Azure Roller | Cloud Glider, Parachute, Flower Glider, Paper Glider |
| 14.4 | 2.986636904613616 | 9139 | 12 | 16 | 15 | 12 | 14 | 12 | 10 | 9 | 8 | 8 | 14 | 11 | 8 | 9 | Bowser, Morton | Pipe Frame | Roller, Azure Roller | Peach Parasol, Parafoil, Bowser Kite, MKTV Parafoil |
| 14.4 | 2.986636904613616 | 9585 | 12 | 19 | 16 | 11 | 14 | 10 | 9 | 9 | 9 | 7 | 14 | 7 | 11 | 8 | Bowser, Morton | Landship | Roller, Azure Roller | Cloud Glider, Parachute, Flower Glider, Paper Glider |
| 14.4 | 2.986636904613616 | 9587 | 12 | 18 | 16 | 11 | 14 | 11 | 9 | 10 | 9 | 6 | 14 | 8 | 10 | 8 | Bowser, Morton | Landship | Roller, Azure Roller | Peach Parasol, Parafoil, Bowser Kite, MKTV Parafoil |
| 14.4 | 2.986636904613616 | 9921 | 12 | 17 | 15 | 12 | 14 | 11 | 10 | 8 | 8 | 9 | 14 | 10 | 9 | 8 | Bowser, Morton | Varmint, City Tripper | Roller, Azure Roller | Cloud Glider, Parachute, Flower Glider, Paper Glider |

The command used to generate this table is:

```bash
python3 find_builds.py  --limit 5 --topk --query-filters min_ground_speed=12 min_acceleration=12 min_miniturbo=5 --query-weights weight_ground_speed=0.5 weight_acceleration=0.5 weight_miniturbo=0.1 --query-sort sort_score=-1 sort_score_dev=-1 --markdown

```

According to the results, the best build is the one with the following build:

- **Driver**: Bowser, Morton
- **Vehicle**: Pipe Frame
- **Tyre**: Roller, Azure Roller
- **Glider**: Cloud Glider, Parachute, Flower Glider, Paper Glider

Yielding the following stats:

- **Ground speed**: 12
- **Acceleration**: 14
- **Miniturbo**: 14
- **Weight**: 11
- **Ground handling**: 10

With a score of 14.4 and a standard deviation of 2.99.

I played a bit with this build, and I can say that it is pretty good.
I feel like it's lacking a little bit of acceleration, but if the player manages to get a good jump ahead of everyone else and build a good gap, it's pretty hard to catch up.
Due to the high score in drifting, I recommend drifting *EVERYWHERE*, even on straight lines, as it will help you to get a good speed up.

## Alternative, better, solutions

Finding the correct weights is however a bit tricky: it's hard to find the "best" build according to parameters that are not well defined.
This is why other algorithms (such as the skyline algorithm) have been created.

I decided to implement $3$ of them:

1. The Medrank algorithm
2. The skyline algorithm
3. The kmeans algorithm

Their results and explanations are shown below.

### Medrank algorithm

The Medrank algorithm allows to compare the stats of the builds without having to rank them according arbitrary weights.
It works by comparing the stats of the builds to the median of the stats of all the builds; the builds with the best mean positions are then selected.

The command to use this algorithm is:

```bash
python3 find_builds.py  --limit 5 --medrank --query-filters min_ground_speed=12 min_acceleration=12 min_miniturbo=5 --ranking-attributes rank_ground_speed=1 rank_miniturbo=1 --query-sort sort_ground_speed=-1 sort_score_dev=-1 --markdown
```

|score|score_dev|id|ground_speed|water_speed|air_speed|antigravity_speed|acceleration|weight|ground_handling|water_handling|air_handling|antigravity_handling|miniturbo|on_road_traction|off_road_traction|invincibility|driver|vehicle|tyre|glider |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 0 | 0 | 672 | 12 | 13 | 15 | 13 | 12 | 10 | 12 | 10 | 11 | 12 | 13 | 10 | 13 | 12 | Mario, Ludwig, Mii (medium) | Standard Bike, Flame Rider, Wild Wiggler, W 25 Silver Arrow | Normal, Normal Blue | Super Glider, Waddle Wing, Hylian Kite |
| 0 | 0 | 674 | 12 | 12 | 15 | 14 | 12 | 11 | 12 | 11 | 11 | 11 | 13 | 11 | 12 | 12 | Mario, Ludwig, Mii (medium) | Standard Bike, Flame Rider, Wild Wiggler, W 25 Silver Arrow | Normal, Normal Blue | Wario Wing, Plane Glider, Gold Glider, Paraglider |
| 0 | 0 | 701 | 12 | 14 | 12 | 14 | 12 | 10 | 10 | 8 | 11 | 11 | 13 | 11 | 14 | 13 | Mario, Ludwig, Mii (medium) | Standard Bike, Flame Rider, Wild Wiggler, W 25 Silver Arrow | Off-Road, Retro Off-Road | Cloud Glider, Parachute, Flower Glider, Paper Glider |
| 0 | 0 | 703 | 12 | 13 | 12 | 14 | 12 | 11 | 10 | 9 | 11 | 10 | 13 | 12 | 13 | 13 | Mario, Ludwig, Mii (medium) | Standard Bike, Flame Rider, Wild Wiggler, W 25 Silver Arrow | Off-Road, Retro Off-Road | Peach Parasol, Parafoil, Bowser Kite, MKTV Parafoil |
| 0 | 0 | 716 | 12 | 13 | 15 | 13 | 12 | 10 | 12 | 10 | 11 | 12 | 13 | 10 | 13 | 13 | Mario, Ludwig, Mii (medium) | Standard Bike, Flame Rider, Wild Wiggler, W 25 Silver Arrow | GLA Wheels | Super Glider, Waddle Wing, Hylian Kite |

The best build according to the Medrank algorithm is the one with the following build:

- **Driver**: Mario, Ludwig, Mii (medium)
- **Vehicle**: Standard Bike, Flame Rider, Wild Wiggler, W 25 Silver Arrow
- **Tyre**: Normal, Normal Blue
- **Glider**: Super Glider, Waddle Wing, Hylian Kite

Yielding the following stats:

- **Ground speed**: 12
- **Acceleration**: 12
- **Miniturbo**: 13
- **Weight**: 10
- **Ground handling**: 12

### Skyline algorithm

The skyline algorithm provides a way to find the best build according to a set of parameters.
It returns a set of tuple, each of which "dominates" the other tuples in the set, following these two rules:

- a tuple must be better than another tuple in at least one of the parameters
- a tuple must be at least as good as another tuple in all the other parameters

As such, only the tuples that are "dominating" other tuples are returned;
this ensures that the builds returned are the best in some way, but not necessarily the best overall.

The command to use this algorithm is:

```bash
python3 find_builds.py --limit 5 --skyline --query-filters min_ground_speed=12 min_acceleration=12 min_miniturbo=5 --query-sort sort_acceleration=-1 sort_ground_speed=-1 --ranking-attributes rank_ground_speed=1 rank_miniturbo=1 --markdown
```

|score|score_dev|id|ground_speed|water_speed|air_speed|antigravity_speed|acceleration|weight|ground_handling|water_handling|air_handling|antigravity_handling|miniturbo|on_road_traction|off_road_traction|invincibility|driver|vehicle|tyre|glider |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 0 | 0 | 11113 | 12 | 17 | 14 | 12 | 14 | 8 | 10 | 10 | 9 | 9 | 14 | 12 | 10 | 9 | Donkey Kong, Waluigi, Roy, Wiggler | Landship | Button, Leaf Tyres | Cloud Glider, Parachute, Flower Glider, Paper Glider |
| 0 | 0 | 12609 | 12 | 19 | 16 | 11 | 14 | 9 | 10 | 10 | 10 | 8 | 14 | 6 | 12 | 7 | Wario, Dry Bowser, Funky Kong | Landship | Roller, Azure Roller | Cloud Glider, Parachute, Flower Glider, Paper Glider |
| 0 | 0 | 9137 | 12 | 17 | 15 | 12 | 14 | 11 | 10 | 8 | 8 | 9 | 14 | 10 | 9 | 9 | Bowser, Morton | Pipe Frame | Roller, Azure Roller | Cloud Glider, Parachute, Flower Glider, Paper Glider |
| 0 | 0 | 13337 | 12 | 19 | 16 | 11 | 14 | 9 | 10 | 10 | 10 | 8 | 14 | 6 | 12 | 8 | Wario, Dry Bowser, Funky Kong | Streetle | Roller, Azure Roller | Cloud Glider, Parachute, Flower Glider, Paper Glider |
| 0 | 0 | 11841 | 12 | 17 | 14 | 12 | 14 | 8 | 10 | 10 | 9 | 9 | 14 | 12 | 10 | 10 | Donkey Kong, Waluigi, Roy, Wiggler | Streetle | Button, Leaf Tyres | Cloud Glider, Parachute, Flower Glider, Paper Glider |

The best build according to the Skyline algorithm is the one with the following build:

- **Driver**: Donkey Kong, Waluigi, Roy, Wiggler
- **Vehicle**: Landship
- **Tyre**: Button, Leaf Tyres
- **Glider**: Cloud Glider, Parachute, Flower Glider, Paper Glider

Yielding the following stats:

- **Ground speed**: 12
- **Acceleration**: 14
- **Miniturbo**: 14
- **Weight**: 8
- **Ground handling**: 10

### Kmeans algorithm

The kmeans algorithm is a clustering algorithm that allows to group the builds according to their stats.
It returns the "centroids" of a set of clusters, which are the builds that are the closest to the mean of the builds in the cluster.

This ensures that the centroid is the most balanced build in the cluster, but it doesn't ensure that it's the best build overall.

The command to use this algorithm is:

```bash
python3 find_builds.py --limit 5 --k-means --query-filters min_ground_speed=12 min_acceleration=12 min_miniturbo=5 --query-sort sort_acceleration=-1 sort_ground_speed=-1 --ranking-attributes rank_ground_speed=1 rank_miniturbo=1 --markdown
```

|score|score_dev|id|ground_speed|water_speed|air_speed|antigravity_speed|acceleration|weight|ground_handling|water_handling|air_handling|antigravity_handling|miniturbo|on_road_traction|off_road_traction|invincibility|driver|vehicle|tyre|glider |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 0 | 0 | 9129 | 14 | 17 | 15 | 14 | 12 | 13 | 9 | 7 | 7 | 8 | 12 | 12 | 10 | 13 | Bowser, Morton | Pipe Frame | Normal, Normal Blue | Cloud Glider, Parachute, Flower Glider, Paper Glider |
| 0 | 0 | 84 | 13 | 15 | 11 | 10 | 12 | 11 | 11 | 9 | 9 | 11 | 13 | 11 | 13 | 13 | Mario, Ludwig, Mii (medium) | Pipe Frame | Off-Road, Retro Off-Road | Super Glider, Waddle Wing, Hylian Kite |
| 0 | 0 | 84 | 13 | 15 | 11 | 10 | 12 | 11 | 11 | 9 | 9 | 11 | 13 | 11 | 13 | 13 | Mario, Ludwig, Mii (medium) | Pipe Frame | Off-Road, Retro Off-Road | Super Glider, Waddle Wing, Hylian Kite |
| 0 | 0 | 1 | 12 | 14 | 14 | 13 | 12 | 10 | 11 | 9 | 12 | 11 | 14 | 10 | 11 | 10 | Mario, Ludwig, Mii (medium) | Standard Kart, The Duke | Normal, Normal Blue | Cloud Glider, Parachute, Flower Glider, Paper Glider |
| 0 | 0 | 1 | 12 | 14 | 14 | 13 | 12 | 10 | 11 | 9 | 12 | 11 | 14 | 10 | 11 | 10 | Mario, Ludwig, Mii (medium) | Standard Kart, The Duke | Normal, Normal Blue | Cloud Glider, Parachute, Flower Glider, Paper Glider |

The best build according to the Kmeans algorithm is the one with the following build:

- **Driver**: Bowser, Morton
- **Vehicle**: Pipe Frame
- **Tyre**: Normal, Normal Blue
- **Glider**: Cloud Glider, Parachute, Flower Glider, Paper Glider

Yielding the following stats:

- **Ground speed**: 14
- **Acceleration**: 12
- **Miniturbo**: 12
- **Weight**: 13
- **Ground handling**: 9

## The code

The code used to create builds is all found in the `find_builds.py` file, while the code used to create the builds is in the `create_builds.py` file.
In order to create the builds, you must run first the latter, then the former.
A database containing the builds will be created in the main folder of the script.

`find_builds.py` accepts the following arguments:

- `--csv` to output the builds in a csv format
- `--json` and `--json-pretty` to output the builds in a json format
- `--markdown` to output the builds in a markdown table format

The minimum and maximum values, the sort order, the weights and the number of builds to be shown can be passed as attributes to the `MK8DeluxeBuilds` class.
A list of available filters, sort orders, and weights can be found respectively in the `available_filters`, `available_sort_orders` and `available_weights` attributes of the `MK8DeluxeBuilds` class.

## The future

In the foreseeable future, I plan to add:

- Tests *(I know, I know)*
- A simple web interface, to make the data more accessible to everyone
- A more informed and sensible way to set the weights and the filters
  - I could even try to simulate the circuits

## Credits

- [Mario Kart 8 Deluxe](https://www.nintendo.com/games/detail/mario-kart-8-deluxe-switch/) for being such a great game
- [Mario Kart 8 Deluxe Wiki](https://www.mariowiki.com/Mario_Kart_8_Deluxe_in-game_statistics) for the stats

The code is distributed under the MIT license.
