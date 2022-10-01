# MK8D-analysis

I have been playing the new Mario Kart on the Nintendo Switch for about a year.
The peculiarity of this game, a new feature introduced in this iteration, is the high level of customization of the karts and the bikes.
Before playing a Grand Prix, either locally or online, the player must choose:

- A **character**
- A **bike** or a **kart**
- The **tyres**
- The **glider**

each of them having 6 visible stats *(ground speed, acceleration, weight, handling, traction, miniturbo)* and 6 more hidden stats *(air speed, antigravity speed, water speed, water handling, air handling, antigravity handling)*.

The question that soon arised was: how do I a choose a setup (character, kart, tyres, glider) that is the best?
*It is possible to finally defeat the superior Japanese players in the 200cc category?*

## The data

All the data has been gathered from the [Mario Kart 8 Deluxe Wiki](https://www.mariowiki.com/Mario_Kart_8_Deluxe).

I soon found that that not each entity is unique;
up to 4 karts, characters, tyres and gliders can share the same stats.

For example the characters *Waluigi*, *Donkey Kong* and *Roy Koopa* all share the same stats; the same goes for the karts *Streetle* and the *Landship*.

In order to reduce the size of the database *(and somehow make the data more manageable)*, I grouped the entities that share the same stats together, by giving them a shared id.
One more table, linking the entity id to their relative names, was needed.

I originally downloaded all the data *(via copy-pasting)* into `csv` files, where I cleaned them.
In order to make the data more accessible and easy to manipulate, I created a `sqlite` database and imported the data into it.

I chose to use `sqlite` because it allows to easily query the data via `SQL`; while not being a language that I particularly like, I figured out that it would have made my life easier in this case.
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

The builds are then saved into another `sqlite` database and inside a (pretty big) `csv` file in order to be used later.

### Find builds

The script `find_builds.py` loads all the created builds in the previous step and filters them according to the user's needs, thanks to the `MK8DeluxeBuilds` class.

In order to do so, the script:

- Accepts a minimum and maximum value for each stat
- Orders the builds in a order according to the user's needs
- Computes a score for each build, according on some custom weights
- Limits the number of builds to be shown

All of these manipulations are done via dunder methods, which makes the code very readable *(I hope)* as it reduces the overall verbosity and makes the code more compact.

The output of the script can be either printed to the console "raw" *(in a human-readable format)*, in `json` or `csv` format.

## The results

Now the hard part is setting custom weights and filters.
How is it possible to balance the stats in order to get the best build?

Long before making this program, I read a lot of online articles and watched a lot of videos discussing the best builds.
Some would prefer acceleration over velocity, others would prefer handling over traction.

After playing for a long while, I found out that:

- Miniturbo is a really important stat, as I get a lot of them due to my continuous drifting
- Acceleration is more important than speed, as online lobbies make an aggressive use of items
- Handling and traction are pretty important, but not as much as the other stats
- The best build is the one that has balanced stats

So I tweaked the weights and the filters, finally setting:

- The minimum ground speed to 12
- The minimum ground acceleration to 12
- The minimum miniturbo to 5
- Ground speed weight to 0.5
- Acceleration weight to 0.5
- Miniturbo weight to 0.1

The top 5 builds, sorted by *score* and the *standard deviation* of the stats, are the following:

| score | score_dev | ground_speed | water_speed | air_speed | antigravity_speed | acceleration | weight | ground_handling | water_handling | air_handling | antigravity_handling |             traction              |                       miniturbo                       |           driver           |                            vehicle                             | tyre  | glider |
| :---: | :-------: | :----------: | :---------: | :-------: | :---------------: | :----------: | :----: | :-------------: | :------------: | :----------: | :------------------: | :-------------------------------: | :---------------------------------------------------: | :------------------------: | :------------------------------------------------------------: | :---: | :----: |
|  12   |    16     |      16      |     13      |    13     |        10         |      10      |   8    |       11        |       10       |      8       |          13          | ['Waluigi', 'Donkey Kong', 'Roy'] |   ['Standard Kart', '300 SL Roadster', 'The Duke']    | ['Roller', 'Azure Roller'] | ['Cloud Glider', 'Parachute', 'Flower Glider', 'Paper Glider'] |
|  12   |    15     |      16      |     13      |    13     |        11         |      10      |   9    |       11        |       9        |      7       |          13          | ['Waluigi', 'Donkey Kong', 'Roy'] |   ['Standard Kart', '300 SL Roadster', 'The Duke']    | ['Roller', 'Azure Roller'] | ['Peach Parasol', 'Parafoil', 'Bowser Kite', 'MKTV Parafoil']  |
|  12   |    15     |      14      |     12      |    13     |        10         |      11      |   9    |        7        |       11       |      8       |          13          | ['Waluigi', 'Donkey Kong', 'Roy'] |       ['Pipe Frame', 'Varmint', 'City Tripper']       |  ['Button', 'Leaf Tires']  |         ['Super Glider', 'Waddle Wing', 'Hylian Kite']         |
|  12   |    14     |      14      |     13      |    13     |        11         |      11      |   10   |        7        |       10       |      7       |          13          | ['Waluigi', 'Donkey Kong', 'Roy'] |       ['Pipe Frame', 'Varmint', 'City Tripper']       |  ['Button', 'Leaf Tires']  |  ['Wario Wing', 'Plane Glider', 'Gold Glider', 'Paraglider']   |
|  12   |    15     |      18      |     12      |    13     |        11         |      11      |   8    |       11        |       10       |      8       |          13          | ['Waluigi', 'Donkey Kong', 'Roy'] | ['Cat Cruiser', 'Comet', 'Yoshi Bike', 'Teddy Buggy'] | ['Roller', 'Azure Roller'] |         ['Super Glider', 'Waddle Wing', 'Hylian Kite']         |

They all share the same score, with slightly varying standard deviation;
then best build, according to these parameter, is then the following:

- Driver: *Waluigi, Donkey Kong, Roy*
- Kart: *Standard Kart, 300 SL Roadster, The Duke*
- Tyre: *Roller, Azure Roller*
- Glider: *Cloud Glider, Parachute, Flower Glider, Paper Glider*

in any combination.

I played a lot with this build, and I can say that it is pretty good.
I feel like it's lacking a little bit of acceleration, but if the player manages to get a good jump ahead of everyone else and build a good gap, it's pretty hard to catch up.
Due to the high score in drifting, I recommend to drift *EVERYWHERE*, even on straight lines, as it will help you to get a good speed up.

## The code

The code used to create builds is all found in the `find_builds.py` file, while the code used to create the builds is in the `create_builds.py` file.
In order to create the builds, you must run first the latter, then the former.
A database containing the builds will be created in the main folder of the script.

`find_builds.py` accepts the following arguments:

- `--csv` to output the builds in a csv format
- `--json` and `--json-pretty` to output the builds in a json format
- `--markdown` to output the builds in a markdown table format

As now, the only way to tweak the parameters and influence the build is to edit the code.
The minimum and maximum values, the sort order, the weights and the number of builds to be shown can be passed as attributes to the `MK8DeluxeBuilds` class.
A list of available filters, sort orders, and weights can be found respectively in the `available_filters`, `available_sort_orders` and `available_weights` attributes of the `MK8DeluxeBuilds` class.

## The future

In the foreseeable future, I plan to add:

- Tests *(I know, I know)*
- A simple web interface, to make the data more accessible to everyone
- Some way of automating the process of finding the best builds
  - if only Nintendo shared some stats about the multiplayer way, I could find a way to auto generate the weights...

## Credits

- [Mario Kart 8 Deluxe](https://www.nintendo.com/games/detail/mario-kart-8-deluxe-switch/) for being such a great game
- [Mario Kart 8 Deluxe Wiki](https://www.mariowiki.com/Mario_Kart_8_Deluxe) for the stats

The code is distributed under the MIT license.
