---
title: Blog
description: A blog about exploring by train and on foot, especially in Málaga province
layout: default
---

# Blog 

## Featured Posts 

{% assign featured = site.posts | where: "feature", "y" %}
{% for post in featured %}
 
 <div class="blogentry">
   <h3><a href="{{ post.url }}">{{ post.title }}</a></h3>
   <p class="postdate">
   {% if post.date %}
     {{ post.date | date_to_string }} 
     {% if post.last_modified_at %}
       &nbsp;(updated {{ post.last_modified_at | date_to_string }}) 
     {% endif %}
   {% endif %}
   </p>
   <p>{{ post.description}}</p>
   {% if post.image-small.path %}
      <a href="{{ post.url }}"><img src= "{{ post.image-small.path}}" alt="{{ post.image.alt}}" width="{{ post.image-small.width }}" height="{{ post.image-small.height }}"></a>
   {% endif %}
 </div>

{% endfor %}

## All Posts

{% for post in site.posts %}

<div class="blogentry">
 
   <h3><a href="{{ post.url }}">{{ post.title }}</a></h3>
   <p class="postdate">
   {% if post.date %}
     {{ post.date | date_to_string }} 
     {% if post.last_modified_at %}
       &nbsp;(updated {{ post.last_modified_at | date_to_string }}) 
     {% endif %}
   {% endif %}
   </p>
   <p>{{ post.description}}</p>
 </div>

{% endfor %}

