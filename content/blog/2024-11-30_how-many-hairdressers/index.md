---
draft: True
description: Thoughts on mapping local pointsof interest in OpenStreetMap.
image:
  alt: Screenshot from the CityStrides website, showing a map of GPS traces overlaid over the city of Malaga, with some statistics. Just over 25% of streets have been completed.
  path: /assets/images/20240510-citystrides-malaga-25pc.jpg
  width: 640
  height: 511
image-small:
  path: /assets/images/small/20240510-citystrides-malaga-25pc.jpg
  width: 320
  height: 256
---
# How many hairdressers does one barrio need? 

Recently I have made a big effort to update data about points of interest near me in [OpenStreetMap](https://www.openstreetmap.org/welcome) (OSM), Here are some thoughts...

## Background

I have a mixed history mapping shops, businesses, and similar points of interest (POIs). It's not something that motivates me in the same way as mapping hiking routes and pedestrian infrastructure. But I recognise that many users of general-purpose map applications based on OSM expect to be able to find points of interest, so from time to time I have made an effort to add this kind of data. But I've never been very systematic about this.

A couple of months ago I decided to map the POIs in a small area of the city of Málaga as thoroughly as possible, and to track the impact of my efforts on the data. 

Málaga is divided into about 200 *barrios* or neighborhoods, all with well-defined boundaries in OSM. I chose an area of four adjoining barrios slightly to the northeast of the historic centre. The main axis of this area, formed by Calle Victoria and Calle Cristo de la Epidemia, is about 1km long. These main thoroughfares, and many of the smaller streets, are lined by apartment blocks with commercial premises on the ground floor. Most shops are quite small - even there few supermarkets in the area are relatively small. There are no shopping malls. 

map of context

Various OSM contributors have added POI data here over the years, with a particularly big effort in 2017. I have updated individual POIs from time to time when I noticed changes, but I was aware that I hadn't been very diligent about this so there was probably quite a lot of outdated data. Still, I reckoned POIs in the area were reasonably well mapped, and that it wouldn'take too long to add some missing shops and update others. 

Spoiler: I was wrong.

<aside>I don't intend to get too technical here. For anyone interested in how I used Overpass, Python, and Pandas to produce the figures quoted here, the details are on [Github](url).</aside>

<img alt="Screenshot from the CityStrides website, showing a map of GPS traces overlaid over the city of Malaga, with some statistics. Just over 25% of streets have been completed." src="/assets/images/20240510-citystrides-malaga-25pc.jpg" width="640" height="511">



Often when walking around the city I am more focused on surveying for [OpenStreetMap](https://www.openstreetmap.org/welcome). These turn out to be nicely complementary activities. CityStrides is based entirely on OpenStreetMap (OSM) data, so using the tool often alerts me to things that need updating in OSM. If I can't complete a street in CityStrides because it is closed to the public, for exam

